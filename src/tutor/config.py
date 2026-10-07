"""Settings shared by every part of the project."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://tutor:tutor@localhost:5432/tutor")
BOOK_DIR = PROJECT_ROOT / "data" / "openstax-physics"
SCHEMA_PATH = PROJECT_ROOT / "db" / "schema.sql"
