"""Measure retrieval quality on the eval set: Recall@5, Recall@10, MRR, by question type,
volume and physics topic.

A hit = any retrieved chunk whose section is one of the case's gold sections.
Gold sections are volume-qualified ("1:5.2") because section numbers repeat across volumes.

Run:  uv run python evals/run_retrieval_eval.py [--methods vector keyword hybrid]
Writes a dated Markdown report to evals/results/.
"""

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from tutor.db import connect
from tutor.retrieve import METHODS, retrieve
from tutor.topics import TOPICS

CASES = Path(__file__).parent / "retrieval_cases.jsonl"
RESULTS = Path(__file__).parent / "results"
DEPTH = 10  # retrieve this many, score Recall@5 and Recall@10 from it


def first_hit_rank(hits, gold: set[str]) -> int | None:
    for rank, hit in enumerate(hits, start=1):
        if hit.ref in gold:
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
    volumes = sorted({int(c["gold"][0].split(":")[0]) for c in cases})  # a case's volume = its first gold section's
    topics = [t for t in TOPICS if any(c["topic"] == t for c in cases)]  # book order
    today = datetime.now().astimezone().date()
    counts = ", ".join(f"{t}: {sum(c['type'] == t for c in cases)}" for t in types)
    topic_counts = ", ".join(f"{t}: {sum(c['topic'] == t for c in cases)}" for t in topics)
    lines = [f"# Retrieval eval, {today}", "",
             f"{len(cases)} cases ({counts}). Hit = a chunk from a gold section.",
             f"By topic: {topic_counts}.", "",
             "| Method | Recall@5 | Recall@10 | MRR | " + " | ".join(f"R@5 {t}" for t in types)
             + " | " + " | ".join(f"R@5 vol {v}" for v in volumes) + " |",
             "|---|---|---|---|" + "---|" * (len(types) + len(volumes))]
    topic_lines = ["", "## Recall@5 by topic", "",
                   "| Method | " + " | ".join(topics) + " |", "|---|" + "---|" * len(topics)]
    misses: dict[str, list[str]] = {}

    with connect() as conn:
        for method in args.methods:
            ranks, by_type, by_volume, by_topic = [], defaultdict(list), defaultdict(list), defaultdict(list)
            misses[method] = []
            for case in cases:
                hits = retrieve(conn, case["question"], k=DEPTH, method=method)
                rank = first_hit_rank(hits, set(case["gold"]))
                ranks.append(rank)
                by_type[case["type"]].append(rank)
                by_volume[int(case["gold"][0].split(":")[0])].append(rank)
                by_topic[case["topic"]].append(rank)
                if rank is None or rank > 5:
                    got = ", ".join(h.ref if h.section_number else f"{h.volume}:intro" for h in hits[:3])
                    misses[method].append(f"- #{case['id']} {case['question']} (gold {'/'.join(case['gold'])}; got {got})")
            s = score(ranks)
            per_type = " | ".join(f"{score(by_type[t])['recall@5']:.0%}" for t in types)
            per_volume = " | ".join(f"{score(by_volume[v])['recall@5']:.0%}" for v in volumes)
            lines.append(f"| {method} | {s['recall@5']:.0%} | {s['recall@10']:.0%} | {s['mrr']:.2f} "
                         f"| {per_type} | {per_volume} |")
            topic_lines.append(f"| {method} | "
                               + " | ".join(f"{score(by_topic[t])['recall@5']:.0%}" for t in topics) + " |")

    # Few cases per topic (one optics question = 50 points), so read these as hints.
    lines += topic_lines
    for method, missed in misses.items():
        lines += ["", f"## Misses outside the top 5: {method} ({len(missed)})", *missed]

    report = "\n".join(lines) + "\n"
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / f"{today}-{'-'.join(args.methods)}.md"
    out.write_text(report)
    print(report)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
