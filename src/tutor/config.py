"""Settings shared by every part of the project."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://tutor:tutor@localhost:5432/tutor")
BOOK_DIR = PROJECT_ROOT / "data" / "openstax-physics"
SCHEMA_PATH = PROJECT_ROOT / "db" / "schema.sql"

# Embedding model: small, free, runs locally. 384-dimension vectors, reads up to 512 tokens.
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384
# bge models expect this prefix on search queries (not on the passages).
QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

# Reranker: a cross-encoder reads (question, passage) together and scores the pair.
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_CANDIDATES = 30  # how many first-stage results the reranker re-sorts

# Answer generation (T5)
ANSWER_MODEL = "claude-opus-5-5"
ANSWER_EFFORT = "medium"
ANSWER_PASSAGES = 5
# $ per million tokens (input, output) for the cost line printed after each answer
PRICES = {"claude-opus-5-5": (4.00, 20.00), "claude-sonnet-5-5": (2.00, 10.00), "claude-haiku-4-5": (1.00, 5.00)}
