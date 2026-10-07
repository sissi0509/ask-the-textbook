# Ask the Textbook

**A grounded physics tutor:** ask a physics question in your own words and get a clear explanation (intuition first, everyday examples, plain words), where every claim is grounded in, and cited from, a real textbook.

Under the hood it's a retrieval-augmented generation (RAG) system: a two-stage hybrid retriever (Postgres full-text search + pgvector, merged with reciprocal rank fusion, then a cross-encoder reranker) feeding Claude. Every layer is measured against an evaluation set, and answers are checked for staying faithful to their sources.

> Physics content comes from [OpenStax *University Physics*](https://openstax.org/details/books/university-physics-volume-1), Volumes 1–3 (CC BY-NC-SA 4.0). It's downloaded locally during setup and never stored in this repo.

## Status

✅ **v1 works end to end:** ask a question in the terminal, get a cited explanation.

```bash
uv run python -m tutor.cli "Why do I lean back when the bus suddenly starts?"
```

## Setup

Requirements: [uv](https://docs.astral.sh/uv/), Docker Desktop.

```bash
cp .env.example .env          # add your ANTHROPIC_API_KEY
docker compose up -d          # Postgres + pgvector on localhost:5432
uv sync                       # Python dependencies

# Download the textbook source (text only, ~19 MB; images skipped)
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/openstax/osbooks-university-physics-bundle.git data/openstax-physics
git -C data/openstax-physics sparse-checkout set META-INF collections modules

# Build the database (all three volumes): structure -> chunks -> embeddings
for v in 1 2 3; do
  uv run python -m tutor.ingest.load_sections --volume $v
  uv run python -m tutor.ingest.load_chunks --volume $v
done
uv run python -m tutor.ingest.embed_chunks    # ~70 s for 5,293 chunks; downloads the model once
uv run pytest                 # tests
```

## Retrieval eval

```bash
uv run python evals/run_retrieval_eval.py   # Recall@5/@10 and MRR for every retrieval method
```

| Method | Recall@5 | MRR | Recall@5 on everyday-wording questions |
|---|---|---|---|
| vector | 95% | 0.90 | 85% |
| keyword | 73% | 0.52 | 55% |
| hybrid (RRF) | 91% | 0.82 | 85% |
| **vector + cross-encoder rerank** (default) | **98%** | **0.94** | **95%** |
| hybrid + cross-encoder rerank | 95% | 0.93 | 85% |

55 cases over all three volumes (5,293 chunks); details and caveats in [docs/DESIGN.md](docs/DESIGN.md).

## Design

- [docs/DESIGN.md](docs/DESIGN.md): decisions and why
- [docs/SCHEMA.md](docs/SCHEMA.md): the tables, with a diagram

## License

Code: MIT. Textbook content: OpenStax, CC BY-NC-SA 4.0 (not included).
