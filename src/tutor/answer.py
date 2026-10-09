"""Write the answer: retrieved passages in, explanation with citations out.

The LLM owns the language; code owns the facts. The model cites passages
by number ([2]); our code turns each number into a section label from the
database and rejects numbers that point to no passage.

Citation gate: an answer must cite at least one passage, and every number it
cites must be a real passage. If not, the model gets its answer back with a
correction and tries again (CITATION_RETRIES times). An answer that still fails
is returned with grounded=False, so the caller can say so instead of showing
it as a normal answer.
"""

import re
from collections.abc import Iterator
from dataclasses import dataclass

import anthropic
import psycopg

from tutor.config import (
    ANSWER_EFFORT,
    ANSWER_MODEL,
    ANSWER_PASSAGES,
    CITATION_RETRIES,
    DEFAULT_METHOD,
    PRICES,
)
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
use to check their understanding. Write equations in plain text with Unicode symbols
(n₁ sin θ₁ = n₂ sin θ₂), never LaTeX: the answer is shown as plain Markdown."""

# Same teaching style, no passages: the baseline for "does retrieval help?"
DIRECT_SYSTEM = """You are a physics tutor. You explain ideas the way a great teacher does:
intuition first, an everyday example the learner can picture, plain words before
technical terms, and then the precise statement or equation showing the same idea.
"The textbook" means OpenStax University Physics, Volumes 1-3.

Keep it short: about 150-250 words. End with one short question the learner can
use to check their understanding. Write equations in plain text with Unicode symbols
(n₁ sin θ₁ = n₂ sin θ₂), never LaTeX: the answer is shown as plain Markdown."""


RETRY_PROMPT = """Your answer did not pass the citation check: {problem}.
Rewrite it. Cite the passage numbers [1]-[{n}] after each claim that comes from them.
If the passages truly don't cover the question, say so plainly, and still cite the
closest passage you used, if any."""


@dataclass
class Answer:
    text: str
    passages: list[Hit]
    cited: list[int]       # passage numbers the answer cites, in order of first use
    invalid: list[int]     # cited numbers that point to no passage
    input_tokens: int      # tokens and cost add up every attempt
    output_tokens: int
    cost_usd: float
    grounded: bool = False  # passed the citation gate (always False with no passages)
    attempts: int = 1


@dataclass
class Retry:
    """Yielded between attempts: the text streamed so far failed the gate."""
    reason: str


def label(hit: Hit) -> str:
    # Every chapter has an "Introduction", so name the chapter for those.
    section = (f"§{hit.section_number} {hit.section_title}" if hit.section_number
               else f"Ch. {hit.chapter_number} {hit.section_title}")
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


def citation_problem(cited: list[int], invalid: list[int]) -> str | None:
    """Why an answer fails the citation gate, or None if it passes."""
    if invalid:
        return f"it cites passages that don't exist ({', '.join(map(str, invalid))})"
    if not cited:
        return "it cites no passages"
    return None


def _usage_cost(usage) -> float:
    price_in, price_out = PRICES.get(ANSWER_MODEL, (0.0, 0.0))
    return (usage.input_tokens * price_in + usage.output_tokens * price_out) / 1e6


def _stream(system: str, messages: list[dict]) -> Iterator[str | anthropic.types.beta.BetaMessage]:
    """Stream text pieces from Claude, then yield the final message."""
    client = anthropic.Anthropic()
    with client.beta.messages.stream(
        model=ANSWER_MODEL,
        max_tokens=16000,  # thinking counts toward this, so leave plenty of room
        system=system,
        output_config={"effort": ANSWER_EFFORT},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=messages,
    ) as stream:
        yield from stream.text_stream
        message = stream.get_final_message()
    if message.stop_reason == "refusal":
        raise RuntimeError("The model declined to answer this question.")
    yield message


def stream_direct_answer(question: str) -> Iterator[str | Answer]:
    """No retrieval: the model answers from its own knowledge. A baseline."""
    for piece in _stream(DIRECT_SYSTEM, [{"role": "user", "content": question}]):
        if isinstance(piece, str):
            yield piece
        else:
            text = "".join(b.text for b in piece.content if b.type == "text")
            yield Answer(text=text, passages=[], cited=[], invalid=[],
                         input_tokens=piece.usage.input_tokens,
                         output_tokens=piece.usage.output_tokens,
                         cost_usd=_usage_cost(piece.usage))


def stream_answer(conn: psycopg.Connection, question: str,
                  method: str = DEFAULT_METHOD) -> Iterator[str | Retry | Answer]:
    """Yield the answer text piece by piece, then the finished Answer.

    If an attempt fails the citation gate, yield a Retry (the caller should
    discard the text so far) and stream the next attempt.
    """
    hits = retrieve(conn, question, k=ANSWER_PASSAGES, method=method)
    prompt = f"Textbook passages:\n\n{build_context(hits)}\n\nLearner's question: {question}"
    messages = [{"role": "user", "content": prompt}]
    input_tokens = output_tokens = 0
    cost = 0.0
    for attempt in range(1, CITATION_RETRIES + 2):
        for piece in _stream(SYSTEM, messages):
            if isinstance(piece, str):
                yield piece
            else:
                message = piece
        text = "".join(b.text for b in message.content if b.type == "text")
        input_tokens += message.usage.input_tokens
        output_tokens += message.usage.output_tokens
        cost += _usage_cost(message.usage)
        cited, invalid = check_citations(text, len(hits))
        problem = citation_problem(cited, invalid)
        if problem is None or attempt > CITATION_RETRIES:
            break
        yield Retry(problem)
        # Show the model its own answer and what was wrong with it.
        messages = messages + [
            {"role": "assistant", "content": text},
            {"role": "user", "content": RETRY_PROMPT.format(problem=problem, n=len(hits))},
        ]
    yield Answer(text=text, passages=hits, cited=cited, invalid=invalid,
                 input_tokens=input_tokens, output_tokens=output_tokens, cost_usd=cost,
                 grounded=problem is None, attempts=attempt)
