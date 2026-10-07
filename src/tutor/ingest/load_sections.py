"""Build the `sections` table from the downloaded book and print the tree.

Run:  uv run python -m tutor.ingest.load_sections [--volume 1]
"""

import argparse
from dataclasses import astuple

from tutor.config import BOOK_DIR
from tutor.db import apply_schema, connect
from tutor.ingest.structure import Section, find_collection, parse_collection

UPSERT = """
INSERT INTO sections (id, volume, unit_title, chapter_number, chapter_title,
                      section_number, section_title, book_position)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO UPDATE SET
    volume = EXCLUDED.volume,
    unit_title = EXCLUDED.unit_title,
    chapter_number = EXCLUDED.chapter_number,
    chapter_title = EXCLUDED.chapter_title,
    section_number = EXCLUDED.section_number,
    section_title = EXCLUDED.section_title,
    book_position = EXCLUDED.book_position
"""


def print_tree(sections: list[Section]) -> None:
    current_chapter = None
    for s in sections:
        if s.chapter_number != current_chapter:
            current_chapter = s.chapter_number
            print(f"Ch {s.chapter_number:<3}{s.chapter_title}")
        print(f"     {s.section_number or '':<6}{s.section_title}  ({s.id})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volume", type=int, default=1)
    args = parser.parse_args()

    collection = find_collection(BOOK_DIR, args.volume)
    sections = parse_collection(collection, BOOK_DIR / "modules", args.volume)

    with connect() as conn:
        apply_schema(conn)
        with conn.cursor() as cur:
            cur.executemany(UPSERT, [astuple(s) for s in sections])
        conn.commit()
        total = conn.execute(
            "SELECT count(*) FROM sections WHERE volume = %s", (args.volume,)
        ).fetchone()[0]

    print_tree(sections)
    chapters = len({s.chapter_number for s in sections})
    print(f"\nVolume {args.volume}: {chapters} chapters, {len(sections)} sections parsed; "
          f"{total} rows in the sections table.")


if __name__ == "__main__":
    main()
