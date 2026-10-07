"""Direct LLM vs. RAG on the same questions.

Part 1, normal questions: both answers side by side (citations, honesty about
gaps, cost, speed). The model already knows this textbook (see the
contamination probe), so correctness alone can't separate them.

Part 2, counterfactual questions: a fact in the book is changed *inside a
transaction that is rolled back afterwards*, so the real data never changes.
If the RAG answer reports the planted value, it followed the retrieved
passage; the direct answer can only report what the model remembers.

Run:  uv run python evals/compare_direct_vs_rag.py      (~28 calls, under $1)
"""

import argparse
import time
from datetime import datetime

from tutor.answer import Answer, label, stream_answer, stream_direct_answer
from tutor.db import connect

NORMAL = [
    "Why do I lean back when the bus suddenly starts?",
    "Why does a spinning ice skater speed up when she pulls her arms in?",
    "Why do I get a small shock when I touch a doorknob after walking across a carpet?",
    "How does a refrigerator keep food cold?",
    "Why do we see a rainbow after it rains?",
    "What is the photoelectric effect?",
    "How do we know the universe is expanding?",
    "What is the origin of redshift: the Doppler effect or relativity? Which one is the real explanation?",
]

# (find in the book, replace with, question, real value to look for, planted value to look for)
COUNTERFACTUALS = [
    ("343 m/s", "296 m/s", "According to the textbook, what is the speed of sound in air at 20°C?", "343", "296"),
    ("9.80 m/s^2", "7.30 m/s^2", "According to the textbook, what is the value of g, the acceleration due to gravity on Earth?", "9.8", "7.3"),
    ("6.67 × 10^(−11)", "5.12 × 10^(−11)", "According to the textbook, what is the value of the universal gravitational constant G?", "6.67", "5.12"),
    ("1.602 × 10^(−19)", "1.875 × 10^(−19)", "According to the textbook, what is the smallest unit of electric charge, e?", "1.602", "1.875"),
    ("1000 kg/m^3", "1250 kg/m^3", "According to the textbook, what is the density of water at 4.0 °C?", "1000", "1250"),
    ("3.00 × 10^8 m/s", "2.40 × 10^8 m/s", "According to the textbook, what is the speed of light in a vacuum?", "3.00", "2.40"),
]


def run(stream) -> tuple[Answer, float]:
    start = time.perf_counter()
    answer = next(piece for piece in stream if isinstance(piece, Answer))
    return answer, time.perf_counter() - start


def verdict(text: str, real: str, planted: str) -> str:
    text = text.replace(",", "")  # "1,000" counts as "1000"
    has_real, has_planted = real in text, planted in text
    if has_planted and not has_real:
        return "followed the source ✅"
    if has_real and not has_planted:
        return "used memory ❌"
    if has_real and has_planted:
        return "mentioned both ⚠️"
    return "neither value ⚠️"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--counterfactual-only", action="store_true")
    args = parser.parse_args()
    today = datetime.now().astimezone().date()
    lines = [f"# Direct LLM vs. RAG, {today}", ""]
    totals = {"direct": [0.0, 0.0], "rag": [0.0, 0.0]}  # cost, seconds

    with connect() as conn:
        # ---------- Part 2 first: counterfactuals, all inside one rolled-back transaction
        lines += ["## Counterfactuals: planted facts (rolled back afterwards)", "",
                  "| Planted change | Question | Direct LLM | RAG |", "|---|---|---|---|"]
        followed, details = 0, ["## Counterfactual answers in full", ""]
        try:
            for find, replace, *_ in COUNTERFACTUALS:
                conn.execute("UPDATE chunks SET content = replace(content, %s, %s) WHERE content LIKE %s",
                             (find, replace, f"%{find}%"))
            for find, replace, question, real, planted in COUNTERFACTUALS:
                direct, t_direct = run(stream_direct_answer(question))
                rag, t_rag = run(stream_answer(conn, question))
                totals["direct"][0] += direct.cost_usd
                totals["direct"][1] += t_direct
                totals["rag"][0] += rag.cost_usd
                totals["rag"][1] += t_rag
                rag_verdict = verdict(rag.text, real, planted)
                followed += rag_verdict.startswith("followed")
                lines.append(f"| {find} → **{replace}** | {question} | "
                             f"{verdict(direct.text, real, planted)} | {rag_verdict} |")
                details += [f"### {find} → {replace}", "", f"**Direct:** {direct.text}", "",
                            f"**RAG:** {rag.text}", ""]
        finally:
            conn.rollback()  # the book goes back to its real values
        lines += ["", f"**RAG followed the planted fact in {followed}/{len(COUNTERFACTUALS)} cases.**", ""]
        if args.counterfactual_only:
            lines += details
            normal = []
        else:
            normal = NORMAL

        # ---------- Part 1: normal questions, side by side
        lines += ["## Normal questions: side by side", ""]
        for question in normal:
            direct, t_direct = run(stream_direct_answer(question))
            rag, t_rag = run(stream_answer(conn, question))
            totals["direct"][0] += direct.cost_usd
            totals["direct"][1] += t_direct
            totals["rag"][0] += rag.cost_usd
            totals["rag"][1] += t_rag
            sources = "; ".join(label(rag.passages[n - 1]) for n in rag.cited
                                if 1 <= n <= len(rag.passages)) or "none"
            lines += [f"### {question}", "",
                      f"**Direct LLM** ({len(direct.text.split())} words, {t_direct:.1f}s, ${direct.cost_usd:.3f})", "",
                      direct.text, "",
                      (f"**RAG** ({len(rag.text.split())} words, {t_rag:.1f}s, ${rag.cost_usd:.3f}; "
                       f"sources: {sources})"), "",
                      rag.text, "", "---", ""]

    if not args.counterfactual_only:
        lines += details
    n = len(normal) + len(COUNTERFACTUALS)
    lines[2:2] = ["| | Total cost | Avg time per answer |", "|---|---|---|",
                  f"| Direct LLM | ${totals['direct'][0]:.2f} | {totals['direct'][1] / n:.1f}s |",
                  f"| RAG | ${totals['rag'][0]:.2f} | {totals['rag'][1] / n:.1f}s |", ""]
    suffix = "counterfactual" if args.counterfactual_only else "direct-vs-rag"
    out = f"evals/results/{today}-{suffix}.md"
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[:22]))
    print(f"\nFull report: {out}")


if __name__ == "__main__":
    main()
