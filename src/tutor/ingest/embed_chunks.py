"""Fill chunks.embedding for every chunk that doesn't have one yet.

Run:  uv run python -m tutor.ingest.embed_chunks [--all]
      --all re-embeds everything (e.g. after changing the model or the heading path)
"""

import argparse
import time

from pgvector.psycopg import register_vector

from tutor.db import apply_schema, connect
from tutor.embeddings import embed_passages, get_model, passage_text

SELECT = """
SELECT c.id, s.chapter_number, s.chapter_title, s.section_number, s.section_title,
       c.subsection_title, c.content
FROM chunks c JOIN sections s ON s.id = c.section_id
{where}
ORDER BY s.book_position, c.position
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="re-embed every chunk")
    args = parser.parse_args()

    with connect() as conn:
        apply_schema(conn)
        register_vector(conn)
        where = "" if args.all else "WHERE c.embedding IS NULL"
        rows = conn.execute(SELECT.format(where=where)).fetchall()
        if not rows:
            print("Every chunk already has an embedding. Use --all to redo them.")
            return

        texts = [passage_text(*row[1:]) for row in rows]
        limit = get_model().max_seq_length
        too_long = sum(len(get_model().tokenizer(t)["input_ids"]) > limit for t in texts)

        start = time.perf_counter()
        vectors = embed_passages(texts)
        seconds = time.perf_counter() - start

        with conn.cursor() as cur:
            cur.executemany(
                "UPDATE chunks SET embedding = %s WHERE id = %s",
                [(vector, row[0]) for vector, row in zip(vectors, rows, strict=True)],
            )
        conn.commit()

    print(f"Embedded {len(rows)} chunks in {seconds:.0f}s "
          f"({len(rows) / seconds:.0f} chunks/s), {vectors.shape[1]} dimensions.")
    print(f"{too_long} chunks are longer than the model's {limit}-token limit "
          f"(their ends are cut off).")


if __name__ == "__main__":
    main()
