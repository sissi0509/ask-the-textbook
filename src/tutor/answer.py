"""Write the answer: retrieved passages in, explanation with citations out.

The LLM owns the language; code owns the facts. The model cites passages
by number ([2]); our code turns each number into a section label from the
database and rejects numbers that point to no passage.
"""

import re
from collections.abc import Iterator
from dataclasses import dataclass

import anthropic
import psycopg

from tutor.config import ANSWER_EFFORT, ANSWER_MODEL, ANSWER_PASSAGES, DEFAULT_METHOD, PRICES
from tutor.retrieve import Hit, retrieve

SYSTEM = """You are a physics tutor. You explain ideas the way a great teacher does:
intuition first, an everyday example the learner can picture, plain words before
technical terms, and then the precise statement or equation showing the same idea.

Grounding rules (these matter more than style):
- Use ONLY the numbered textbook passages for physics facts, definitions and equations.
- After each claim that comes from a passage, cite it like [2]. Cite only passages you were given.
- If the passages don't cover part of the question, say so plainly, e.g. "The book passages
  I have don't cover X." Don't fill the gap from memory.
- Never invent quotations from anyone.

Keep it short: about 150-250 words. End with one short question the learner can
use to check their understanding."""

# Same teaching style, no passages: the baseline for "does retrieval help?"
DIRECT_SYSTEM = """You are a physics tutor. You explain ideas the way a great teacher does:
intuition first, an everyday example the learner can picture, plain words before
technical terms, and then the precise statement or equation showing the same idea.
"The textbook" means OpenStax University Physics, Volumes 1-3.

Keep it short: about 150-250 words. End with one short question the learner can
use to check their understanding."""


@dataclass
class Answer:
    text: str
    passages: list[Hit]
    cited: list[int]       # passage numbers the answer cites, in order of first use
    invalid: list[int]     # cited numbers that point to no passage
    input_tokens: int
    output_tokens: int
    cost_usd: float


def label(hit: Hit) -> str:
    section = f"§{hit.section_number} {hit.section_title}" if hit.section_number else hit.section_title
    section = f"Vol. {hit.volume} {section}"
    return f"{section} › {hit.subsection_title}" if hit.subsection_title else section


def build_context(hits: list[Hit]) -> str:
    return "\n\n".join(f"[{i}] {label(h)}\n{h.content}" for i, h in enumerate(hits, start=1))


def check_citations(text: str, n_passages: int) -> tuple[list[int], list[int]]:
    """Return (cited passage numbers in first-use order, numbers outside 1..n_passages)."""
    numbers = [int(n) for group in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", text)
               for n in re.split(r"\s*,\s*", group)]
    cited = list(dict.fromkeys(numbers))
    return cited, [n for n in cited if not 1 <= n <= n_passages]


def _usage_cost(usage) -> float:
    price_in, price_out = PRICES.get(ANSWER_MODEL, (0.0, 0.0))
    return (usage.input_tokens * price_in + usage.output_tokens * price_out) / 1e6


def _stream(system: str, prompt: str) -> Iterator[str | anthropic.types.beta.BetaMessage]:
    """Stream text pieces from Claude, then yield the final message."""
    client = anthropic.Anthropic()
    with client.beta.messages.stream(
        model=ANSWER_MODEL,
        max_tokens=16000,  # thinking counts toward this, so leave plenty of room
        system=system,
        output_config={"effort": ANSWER_EFFORT},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        yield from stream.text_stream
        message = stream.get_final_message()
    if message.stop_reason == "refusal":
        raise RuntimeError("The model declined to answer this question.")
    yield message


def stream_direct_answer(question: str) -> Iterator[str | Answer]:
    """No retrieval: the model answers from its own knowledge. A baseline."""
    for piece in _stream(DIRECT_SYSTEM, question):
        if isinstance(piece, str):
            yield piece
        else:
            text = "".join(b.text for b in piece.content if b.type == "text")
            yield Answer(text=text, passages=[], cited=[], invalid=[],
                         input_tokens=piece.usage.input_tokens,
                         output_tokens=piece.usage.output_tokens,
                         cost_usd=_usage_cost(piece.usage))


def stream_answer(conn: psycopg.Connection, question: str,
                  method: str = DEFAULT_METHOD) -> Iterator[str | Answer]:
    """Yield the answer text piece by piece, then the finished Answer."""
    hits = retrieve(conn, question, k=ANSWER_PASSAGES, method=method)
    prompt = f"Textbook passages:\n\n{build_context(hits)}\n\nLearner's question: {question}"
    for piece in _stream(SYSTEM, prompt):
        if isinstance(piece, str):
            yield piece
        else:
            text = "".join(b.text for b in piece.content if b.type == "text")
            cited, invalid = check_citations(text, len(hits))
            yield Answer(text=text, passages=hits, cited=cited, invalid=invalid,
                         input_tokens=piece.usage.input_tokens,
                         output_tokens=piece.usage.output_tokens,
                         cost_usd=_usage_cost(piece.usage))
