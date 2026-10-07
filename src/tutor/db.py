"""Database helpers."""

import psycopg

from tutor.config import DATABASE_URL, SCHEMA_PATH


def connect() -> psycopg.Connection:
    return psycopg.connect(DATABASE_URL)


def apply_schema(conn: psycopg.Connection) -> None:
    """Create tables if they don't exist yet."""
    conn.execute(SCHEMA_PATH.read_text())
    conn.commit()
