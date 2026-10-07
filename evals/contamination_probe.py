"""How much does the LLM already know about our textbook *without* retrieval?

If the model has memorized the book, a good answer could come from memory
instead of from retrieval, and the eval can't tell them apart (contamination).
Two cheap probes, each compared with what our retriever finds:

  1. Section recall: "Which section of OpenStax University Physics Vol 1 covers X?"
     The model answers from memory; the retriever answers from the database.
  2. Verbatim continuation: give the first ~15 words of a real paragraph and ask
     the model to continue it word for word. High overlap = memorized text.

Run:  uv run python evals/contamination_probe.py      (about 18 short API calls)
"""

import re
from datetime import datetime

import anthropic

from tutor.db import connect
from tutor.retrieve import retrieve

MODEL = "claude-opus-5-5"
BOOK = "OpenStax University Physics, Volume 1"

SECTION_QUESTIONS = [
    ("Why do I lean back when the bus suddenly starts?", "5.2"),
    ("Why does a spinning skater speed up when she pulls her arms in?", "11.3"),
    ("Why does a huge steel ship float?", "14.4"),
    ("What is the parallel axis theorem?", "10.5"),
    ("What are Kepler's laws of planetary motion?", "13.5"),
    ("Why do two slightly out-of-tune guitar strings make a wah-wah sound?", "17.6"),
    ("What is the difference between conservative and non-conservative forces?", "8.2"),
    ("How does a rocket move in empty space?", "9.7"),
]

# Paragraphs to probe for memorization: (section, first words of a chunk).
CONTINUATION_SECTIONS = ["5.2", "11.3", "14.6", "9.7", "17.7"]
PROMPT_WORDS = 15
COMPARE_WORDS = 25

client = anthropic.Anthropic()


def ask(prompt: str, max_tokens: int = 4000) -> str:
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        output_config={"effort": "low"},  # short factual recall; keep it cheap
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": prompt}],
    )
    if response.stop_reason == "refusal":
        return "(refused)"
    # Thinking counts toward max_tokens; too small a limit leaves no visible answer.
    if response.stop_reason == "max_tokens":
        return "(ran out of tokens)"
    return "".join(block.text for block in response.content if block.type == "text").strip()


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def overlap(predicted: str, actual: str) -> float:
    """Share of the actual next words that the model reproduced, in order (LCS)."""
    a, b = words(predicted)[:COMPARE_WORDS + 10], words(actual)[:COMPARE_WORDS]
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)):
            table[i + 1][j + 1] = table[i][j] + 1 if a[i] == b[j] else max(table[i][j + 1], table[i + 1][j])
    return table[-1][-1] / len(b) if b else 0.0


def main() -> None:
    lines = [f"# Contamination probe, {datetime.now().astimezone().date()}", "",
             f"Model: `{MODEL}` (effort low), no retrieval. Book: {BOOK}.", "",
             "## 1. Section recall: memory (LLM) vs. retrieval (our RAG)", "",
             "| Question | Truth | LLM from memory | RAG top hit |", "|---|---|---|---|"]
    llm_right = rag_right = 0
    with connect() as conn:
        for question, truth in SECTION_QUESTIONS:
            answer = ask(f"In {BOOK} (OpenStax, 2016), which numbered section covers this: "
                         f"\"{question}\"? Reply with only the section number and title, "
                         f"like \"3.2 Instantaneous Velocity and Speed\".")
            llm_section = (re.findall(r"\b\d{1,2}\.\d{1,2}\b", answer) or ["?"])[0]
            top = retrieve(conn, question, k=1, method="hybrid_rerank")[0]
            llm_right += llm_section == truth
            rag_right += top.ref == f"1:{truth}"
            lines.append(f"| {question} | {truth} | {answer} {'✅' if llm_section == truth else '❌'} | "
                         f"{top.section_number} {top.section_title} {'✅' if top.ref == f'1:{truth}' else '❌'} |")
        n = len(SECTION_QUESTIONS)
        lines += ["", f"**LLM from memory: {llm_right}/{n} · RAG: {rag_right}/{n}**", "",
                  "## 2. Verbatim continuation (memorization)", "",
                  (f"First {PROMPT_WORDS} words of a real paragraph → model continues; "
                   f"score = share of the true next {COMPARE_WORDS} words reproduced in order."), "",
                  "| Section | Prompt | Model continued | Actual next words | Overlap |", "|---|---|---|---|---|"]
        scores = []
        for section in CONTINUATION_SECTIONS:
            content = conn.execute(
                """SELECT c.content FROM chunks c JOIN sections s ON s.id = c.section_id
                   WHERE s.section_number = %s AND c.chunk_type = 'text'
                     AND array_length(regexp_split_to_array(c.content, '\\s+'), 1) > 60
                   ORDER BY c.position LIMIT 1""", (section,)).fetchone()[0]
            tokens = content.split()
            prompt, actual = " ".join(tokens[:PROMPT_WORDS]), " ".join(tokens[PROMPT_WORDS:PROMPT_WORDS + COMPARE_WORDS])
            answer = ask(f"This passage is from {BOOK}. Continue it word for word with the next "
                         f"{COMPARE_WORDS} words exactly as the book has them. Output only the "
                         f"continuation. If you don't know the exact text, reply UNKNOWN.\n\n\"{prompt}\"",
                         max_tokens=200)
            attempted = not (answer.startswith("(") or answer.upper().startswith("UNKNOWN"))
            score = overlap(answer, actual) if attempted else 0.0
            scores.append(score)
            shown = f"{score:.0%}" if attempted else "no attempt"
            lines.append(f"| {section} | {prompt} … | {answer} | {actual} | {shown} |")
        lines += ["", f"**Average verbatim overlap: {sum(scores) / len(scores):.0%}**"]

    report = "\n".join(lines) + "\n"
    out = f"evals/results/{datetime.now().astimezone().date()}-contamination-probe.md"
    with open(out, "w") as f:
        f.write(report)
    print(report)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
