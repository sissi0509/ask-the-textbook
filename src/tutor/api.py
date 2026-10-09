"""HTTP API for the chat frontend.

Run:  uv run uvicorn tutor.api:app --reload --port 8000

Answers stream as NDJSON (one JSON object per line), so the page can show
text as it's written:
    {"type": "text", "text": "Imagine a "}
    {"type": "text", "text": "tablecloth..."}
    {"type": "retry", "reason": "it cites no passages"}   (failed the citation gate:
                                                           drop the text so far)
    {"type": "done", "answer": {...sources, passages, grounded, cost...}}
    {"type": "error", "message": "..."}      (instead of "done", if it fails)
"""

import json
from collections.abc import Iterator
from contextlib import asynccontextmanager

import anthropic
import psycopg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from tutor import embeddings, rerank
from tutor.answer import Answer, Retry, label, stream_answer, stream_direct_answer
from tutor.config import DEFAULT_METHOD, FRONTEND_ORIGINS
from tutor.db import connect
from tutor.retrieve import METHODS


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load both local models at startup, so the first question isn't slow.
    embeddings.get_model()
    rerank.get_model()
    yield


app = FastAPI(title="Ask the Textbook", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    method: str = DEFAULT_METHOD


def answer_json(answer: Answer) -> dict:
    return {
        "text": answer.text,
        "sources": [
            {"n": n, "label": label(answer.passages[n - 1]), "ref": answer.passages[n - 1].ref}
            for n in answer.cited if 1 <= n <= len(answer.passages)
        ],
        "invalid_citations": answer.invalid,
        "grounded": answer.grounded,
        "attempts": answer.attempts,
        "passages": [{"n": i, "label": label(h), "content": h.content}
                     for i, h in enumerate(answer.passages, start=1)],
        "input_tokens": answer.input_tokens,
        "output_tokens": answer.output_tokens,
        "cost_usd": round(answer.cost_usd, 4),
    }


def ndjson(stream: Iterator[str | Retry | Answer]) -> Iterator[str]:
    try:
        for piece in stream:
            if isinstance(piece, Answer):
                yield json.dumps({"type": "done", "answer": answer_json(piece)}) + "\n"
            elif isinstance(piece, Retry):
                yield json.dumps({"type": "retry", "reason": piece.reason}) + "\n"
            else:
                yield json.dumps({"type": "text", "text": piece}) + "\n"
    # The stream has already started (HTTP 200 sent), so errors are reported in-band.
    # RuntimeError = the model declined (see answer.py).
    except (anthropic.APIError, psycopg.Error, RuntimeError) as error:
        yield json.dumps({"type": "error", "message": str(error)}) + "\n"


def with_connection(question: Question) -> Iterator[str]:
    with connect() as conn:
        yield from ndjson(stream_answer(conn, question.question, method=question.method))


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/methods")
def methods() -> dict:
    return {"methods": list(METHODS), "default": DEFAULT_METHOD}


@app.post("/ask")
def ask(question: Question) -> StreamingResponse:
    """Grounded answer: retrieve passages, then explain with citations."""
    if question.method not in METHODS:
        question.method = DEFAULT_METHOD
    return StreamingResponse(with_connection(question), media_type="application/x-ndjson")


@app.post("/ask/direct")
def ask_direct(question: Question) -> StreamingResponse:
    """Baseline: the model answers from memory, with no retrieval."""
    return StreamingResponse(ndjson(stream_direct_answer(question.question)),
                             media_type="application/x-ndjson")
