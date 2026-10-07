# Learn Physics with Feynman

Ask a physics question and get an explanation in the spirit of Richard Feynman: intuition first, everyday examples, plain words. Every answer is grounded in a real textbook, with citations you can check.

Under the hood it's a retrieval-augmented generation (RAG) system: a two-stage hybrid retriever (Postgres full-text search + pgvector, merged with reciprocal rank fusion, then a cross-encoder reranker) feeding Claude. Every layer is measured against an evaluation set.

> **Not affiliated** with Richard Feynman's estate, Caltech, or *The Feynman Lectures on Physics*, and contains none of their text. "Feynman" here describes a teaching style. Physics content comes from [OpenStax *University Physics*](https://openstax.org/details/books/university-physics-volume-1) (CC BY-NC-SA 4.0), which is downloaded locally during setup and never stored in this repo.

## Status

🚧 v1 in progress: ask a question → Feynman-style answer with citations, plus a retrieval eval baseline.

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
uv run pytest                 # tests
```

## Design

- [docs/DESIGN.md](docs/DESIGN.md): decisions and why
- [docs/SCHEMA.md](docs/SCHEMA.md): the tables, with a diagram

## License

Code: MIT. Textbook content: OpenStax, CC BY-NC-SA 4.0 (not included).
