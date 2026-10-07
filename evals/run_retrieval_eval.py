"""Measure retrieval quality on the eval set: Recall@5, Recall@10, MRR, by question type.

A hit = any retrieved chunk whose section is one of the case's gold sections.

Run:  uv run python evals/run_retrieval_eval.py [--methods vector keyword hybrid]
Writes a dated Markdown report to evals/results/.
"""

import argparse
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

from tutor.db import connect
from tutor.retrieve import METHODS, retrieve

CASES = Path(__file__).parent / "retrieval_cases.jsonl"
RESULTS = Path(__file__).parent / "results"
DEPTH = 10  # retrieve this many, score Recall@5 and Recall@10 from it


def first_hit_rank(hits, gold: set[str]) -> int | None:
    for rank, hit in enumerate(hits, start=1):
        if hit.section_number in gold:
            return rank
    return None


def score(ranks: list[int | None]) -> dict[str, float]:
    n = len(ranks)
    return {
        "recall@5": sum(r is not None and r <= 5 for r in ranks) / n,
        "recall@10": sum(r is not None for r in ranks) / n,
        "mrr": sum(1 / r for r in ranks if r) / n,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", nargs="+", default=list(METHODS), choices=list(METHODS))
    args = parser.parse_args()

    cases = [json.loads(line) for line in CASES.read_text().splitlines() if line.strip()]
    types = sorted({c["type"] for c in cases})
    lines = [f"# Retrieval eval, {date.today()}", "",
             f"{len(cases)} cases ({', '.join(f'{t}: {sum(c['type'] == t for c in cases)}' for t in types)}). "
             "Hit = a chunk from a gold section.", "",
             "| Method | Recall@5 | Recall@10 | MRR | " + " | ".join(f"R@5 {t}" for t in types) + " |",
             "|---|---|---|---|" + "---|" * len(types)]
    misses: dict[str, list[str]] = {}

    with connect() as conn:
        for method in args.methods:
            ranks, by_type = [], defaultdict(list)
            misses[method] = []
            for case in cases:
                hits = retrieve(conn, case["question"], k=DEPTH, method=method)
                rank = first_hit_rank(hits, set(case["gold"]))
                ranks.append(rank)
                by_type[case["type"]].append(rank)
                if rank is None or rank > 5:
                    got = ", ".join(h.section_number or "intro" for h in hits[:3])
                    misses[method].append(f"- #{case['id']} {case['question']} (gold {'/'.join(case['gold'])}; got {got})")
            s = score(ranks)
            per_type = " | ".join(f"{score(by_type[t])['recall@5']:.0%}" for t in types)
            lines.append(f"| {method} | {s['recall@5']:.0%} | {s['recall@10']:.0%} | {s['mrr']:.2f} | {per_type} |")

    for method, missed in misses.items():
        lines += ["", f"## Misses outside the top 5: {method} ({len(missed)})", *missed]

    report = "\n".join(lines) + "\n"
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / f"{date.today()}-{'-'.join(args.methods)}.md"
    out.write_text(report)
    print(report)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
