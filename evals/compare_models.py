"""Compare embedding models and rerankers on the retrieval eval set.

For each embedding model: vector search alone, then vector + each reranker
(the app's default pipeline, vector_rerank). Reports Recall@5, Recall@10, MRR,
and average search time per question.

First embed the chunks with every extra model (once, a few minutes each):
      uv run python -m tutor.ingest.embed_chunks --model BAAI/bge-base-en-v1.5
      uv run python -m tutor.ingest.embed_chunks --model sentence-transformers/all-MiniLM-L6-v2
Run:  uv run python evals/compare_models.py
Writes a dated Markdown report to evals/results/.
"""

import json
import time
from datetime import datetime

from run_retrieval_eval import CASES, DEPTH, RESULTS, first_hit_rank, score

from tutor.config import EMBEDDING_MODEL, EMBEDDING_MODELS, RERANK_MODELS
from tutor.db import connect
from tutor.retrieve import vector_rerank_search, vector_search


def short(model: str) -> str:
    return model.split("/")[-1]


def run(conn, cases, search) -> tuple[dict[str, float], float]:
    """Scores for one pipeline, plus its average milliseconds per question."""
    search(conn, cases[0]["question"], DEPTH)  # warm-up: load the models before timing
    ranks, start = [], time.perf_counter()
    for case in cases:
        ranks.append(first_hit_rank(search(conn, case["question"], DEPTH), set(case["gold"])))
    ms = (time.perf_counter() - start) * 1000 / len(cases)
    return score(ranks), ms


def missing_models(conn) -> list[str]:
    stored = {m for (m,) in conn.execute("SELECT DISTINCT model FROM chunk_embeddings")}
    return [m for m in EMBEDDING_MODELS if m != EMBEDDING_MODEL and m not in stored]


def main() -> None:
    cases = [json.loads(line) for line in CASES.read_text().splitlines() if line.strip()]
    today = datetime.now().astimezone().date()
    lines = [f"# Model comparison, {today}", "",
             (f"{len(cases)} cases. Hit = a chunk from a gold section. "
              "Reranking re-sorts the top 30 vector results. "
              "Time = average per question on this machine."), "",
             "| Embedding model | Reranker | Recall@5 | Recall@10 | MRR | ms / question |",
             "|---|---|---|---|---|---|"]

    with connect() as conn:
        if missing := missing_models(conn):
            raise SystemExit("Embed these models first:\n" + "\n".join(
                f"  uv run python -m tutor.ingest.embed_chunks --model {m}" for m in missing))

        for emb in EMBEDDING_MODELS:
            pipelines = [("none", lambda c, q, k, e=emb: vector_search(c, q, k, embedding_model=e))]
            pipelines += [(short(r), lambda c, q, k, e=emb, r=r: vector_rerank_search(
                c, q, k, embedding_model=e, rerank_model=r)) for r in RERANK_MODELS]
            for reranker, search in pipelines:
                s, ms = run(conn, cases, search)
                row = (f"| {short(emb)} | {reranker} | {s['recall@5']:.0%} | {s['recall@10']:.0%} "
                       f"| {s['mrr']:.2f} | {ms:.0f} |")
                lines.append(row)
                print(row, flush=True)

    report = "\n".join(lines) + "\n"
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / f"{today}-model-comparison.md"
    out.write_text(report)
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
