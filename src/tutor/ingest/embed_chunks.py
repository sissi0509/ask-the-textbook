"""Fill chunks.embedding for every chunk that doesn't have one yet.

Run:  uv run python -m tutor.ingest.embed_chunks [--all] [--model NAME]
      --all re-embeds everything (e.g. after changing the model or the heading path)
      --model embeds with another model into chunk_embeddings, for the model comparison
"""

import argparse
import time

from pgvector.psycopg import register_vector

from tutor.config import EMBEDDING_MODEL, EMBEDDING_MODELS
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
    parser.add_argument("--model", default=EMBEDDING_MODEL, choices=list(EMBEDDING_MODELS))
    args = parser.parse_args()
    default = args.model == EMBEDDING_MODEL

    with connect() as conn:
        apply_schema(conn)
        register_vector(conn)
        if args.all:
            where = ""
        elif default:
            where = "WHERE c.embedding IS NULL"
        else:
            where = ("WHERE NOT EXISTS (SELECT 1 FROM chunk_embeddings e "
                     "WHERE e.chunk_id = c.id AND e.model = %(model)s)")
        rows = conn.execute(SELECT.format(where=where), {"model": args.model}).fetchall()
        if not rows:
            print("Every chunk already has an embedding. Use --all to redo them.")
            return

        texts = [passage_text(*row[1:]) for row in rows]
        model = get_model(args.model)
        limit = model.max_seq_length
        too_long = sum(len(model.tokenizer(t)["input_ids"]) > limit for t in texts)

        start = time.perf_counter()
        vectors = embed_passages(texts, model=args.model)
        seconds = time.perf_counter() - start

        with conn.cursor() as cur:
            if default:
                cur.executemany(
                    "UPDATE chunks SET embedding = %s WHERE id = %s",
                    [(vector, row[0]) for vector, row in zip(vectors, rows, strict=True)],
                )
            else:
                cur.executemany(
                    """INSERT INTO chunk_embeddings (chunk_id, model, embedding)
                       VALUES (%s, %s, %s)
                       ON CONFLICT (chunk_id, model) DO UPDATE SET embedding = EXCLUDED.embedding""",
                    [(row[0], args.model, vector) for vector, row in zip(vectors, rows, strict=True)],
                )
        conn.commit()

    print(f"Embedded {len(rows)} chunks in {seconds:.0f}s "
          f"({len(rows) / seconds:.0f} chunks/s), {vectors.shape[1]} dimensions.")
    print(f"{too_long} chunks are longer than the model's {limit}-token limit "
          f"(their ends are cut off).")


if __name__ == "__main__":
    main()
