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
