"""Chunk every section of a volume into the `chunks` table, and store summaries.

Needs the `sections` table first (tutor.ingest.load_sections).
Re-running replaces the volume's chunks, so changing the chunking rules is safe.

Run:  uv run python -m tutor.ingest.load_chunks [--volume 1]
"""

import argparse
import statistics
from collections import Counter

from tutor.config import BOOK_DIR
from tutor.db import apply_schema, connect
from tutor.ingest.chunking import parse_module


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volume", type=int, default=1)
    args = parser.parse_args()

    types: Counter[str] = Counter()
    word_counts: list[int] = []
    empty_sections: list[str] = []

    with connect() as conn:
        apply_schema(conn)
        section_ids = [
            row[0]
            for row in conn.execute(
                "SELECT id FROM sections WHERE volume = %s ORDER BY book_position", (args.volume,)
            )
        ]
        if not section_ids:
            raise SystemExit("No sections found. Run tutor.ingest.load_sections first.")

        with conn.cursor() as cur:
            for section_id in section_ids:
                module = parse_module(BOOK_DIR / "modules" / section_id)
                cur.execute("UPDATE sections SET summary = %s WHERE id = %s",
                            (module.summary, section_id))
                cur.execute("DELETE FROM chunks WHERE section_id = %s", (section_id,))
                cur.executemany(
                    "INSERT INTO chunks (section_id, position, subsection_title, chunk_type, content)"
                    " VALUES (%s, %s, %s, %s, %s)",
                    [(section_id, c.position, c.subsection_title, c.chunk_type, c.content)
                     for c in module.chunks],
                )
                if not module.chunks:
                    empty_sections.append(section_id)
                types.update(c.chunk_type for c in module.chunks)
                word_counts += [len(c.content.split()) for c in module.chunks if c.chunk_type == "text"]
        conn.commit()

        summaries = conn.execute(
            "SELECT count(summary) FROM sections WHERE volume = %s", (args.volume,)
        ).fetchone()[0]

    print(f"Volume {args.volume}: {len(section_ids)} sections -> {sum(types.values())} chunks")
    for chunk_type, n in types.most_common():
        print(f"  {chunk_type:<11}{n}")
    print(f"Text chunk words: median {statistics.median(word_counts):.0f}, "
          f"min {min(word_counts)}, max {max(word_counts)}")
    print(f"Sections with a summary: {summaries}")
    print(f"Sections with no chunks: {empty_sections or 'none'}")


if __name__ == "__main__":
    main()
