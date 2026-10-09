"""Find the chunks most relevant to a question.

Each method adds one layer, so the eval can measure what every layer adds:
  vector          meaning: cosine distance between question and chunk embeddings
  keyword         exact words: Postgres full-text search
  hybrid          both, merged with Reciprocal Rank Fusion (RRF)
  vector_rerank   vector top 30, re-sorted by a cross-encoder
  hybrid_rerank   hybrid top 30, re-sorted by a cross-encoder
"""

from dataclasses import dataclass

import psycopg
from pgvector.psycopg import register_vector

from tutor.config import EMBEDDING_MODEL, RERANK_CANDIDATES, RERANK_MODEL
from tutor.embeddings import embed_query
from tutor.rerank import rerank_scores

RRF_K = 60          # standard RRF constant: dampens the gap between rank 1 and rank 2
CANDIDATES = 50     # how many results each path contributes before fusion

COLUMNS = """
    c.id, c.section_id, s.section_number, s.section_title,
    c.subsection_title, c.chunk_type, c.content
"""
# score comes next in every SELECT; volume and chapter are selected last
VOLUME = ", s.volume, s.chapter_number"


@dataclass
class Hit:
    chunk_id: int
    section_id: str
    section_number: str | None
    section_title: str
    subsection_title: str | None
    chunk_type: str
    content: str
    score: float
    volume: int = 1
    chapter_number: int = 0

    @property
    def ref(self) -> str:
        """Volume-qualified section, e.g. '1:5.2'. Section numbers repeat across volumes."""
        return f"{self.volume}:{self.section_number}"


def vector_search(
    conn: psycopg.Connection, question: str, k: int, embedding_model: str = EMBEDDING_MODEL
) -> list[Hit]:
    register_vector(conn)
    q = embed_query(question, model=embedding_model)
    if embedding_model == EMBEDDING_MODEL:
        sql = f"""SELECT {COLUMNS}, 1 - (c.embedding <=> %(q)s) AS score{VOLUME}
            FROM chunks c JOIN sections s ON s.id = c.section_id
            ORDER BY c.embedding <=> %(q)s
            LIMIT %(k)s"""
    else:
        # Other models' vectors live in chunk_embeddings (one row per chunk per model).
        sql = f"""SELECT {COLUMNS}, 1 - (e.embedding <=> %(q)s) AS score{VOLUME}
            FROM chunk_embeddings e
            JOIN chunks c ON c.id = e.chunk_id
            JOIN sections s ON s.id = c.section_id
            WHERE e.model = %(model)s
            ORDER BY e.embedding <=> %(q)s
            LIMIT %(k)s"""
    rows = conn.execute(sql, {"q": q, "k": k, "model": embedding_model}).fetchall()
    return [Hit(*row) for row in rows]


def keyword_search(conn: psycopg.Connection, question: str, k: int) -> list[Hit]:
    # plainto_tsquery ANDs every word ("lean & back & bus & start"), so a
    # question rarely matches anything. Swapping & for | means "any of these
    # words", and ts_rank_cd ranks chunks that match more of them higher.
    rows = conn.execute(
        f"""WITH q AS (
                SELECT replace(plainto_tsquery('english', %(q)s)::text, '&', '|')::tsquery AS query
            )
            SELECT {COLUMNS}, ts_rank_cd(c.search_vector, q.query) AS score{VOLUME}
            FROM chunks c JOIN sections s ON s.id = c.section_id, q
            WHERE c.search_vector @@ q.query
            ORDER BY score DESC
            LIMIT %(k)s""",
        {"q": question, "k": k},
    ).fetchall()
    return [Hit(*row) for row in rows]


def rrf_merge(result_lists: list[list[Hit]], k: int) -> list[Hit]:
    """Reciprocal Rank Fusion: score = sum over lists of 1 / (RRF_K + rank).

    Uses ranks, not scores, because cosine similarity and ts_rank are on
    different scales. A chunk near the top of both lists wins.
    """
    scores: dict[int, float] = {}
    hits: dict[int, Hit] = {}
    for results in result_lists:
        for rank, hit in enumerate(results, start=1):
            scores[hit.chunk_id] = scores.get(hit.chunk_id, 0.0) + 1 / (RRF_K + rank)
            hits.setdefault(hit.chunk_id, hit)
    best = sorted(scores, key=scores.get, reverse=True)[:k]
    return [Hit(**{**hits[i].__dict__, "score": scores[i]}) for i in best]


def hybrid_search(conn: psycopg.Connection, question: str, k: int) -> list[Hit]:
    return rrf_merge(
        [vector_search(conn, question, CANDIDATES), keyword_search(conn, question, CANDIDATES)],
        k,
    )


def rerank(question: str, candidates: list[Hit], k: int, model: str = RERANK_MODEL) -> list[Hit]:
    """Second stage: re-sort first-stage candidates by cross-encoder score."""
    if not candidates:
        return []
    passages = [
        " › ".join(filter(None, [h.section_title, h.subsection_title])) + "\n" + h.content
        for h in candidates
    ]
    scores = rerank_scores(question, passages, model=model)
    ranked = sorted(zip(candidates, scores, strict=True), key=lambda pair: pair[1], reverse=True)
    return [Hit(**{**hit.__dict__, "score": float(score)}) for hit, score in ranked[:k]]


def vector_rerank_search(
    conn: psycopg.Connection, question: str, k: int,
    embedding_model: str = EMBEDDING_MODEL, rerank_model: str = RERANK_MODEL,
) -> list[Hit]:
    candidates = vector_search(conn, question, RERANK_CANDIDATES, embedding_model)
    return rerank(question, candidates, k, model=rerank_model)


def hybrid_rerank_search(conn: psycopg.Connection, question: str, k: int) -> list[Hit]:
    return rerank(question, hybrid_search(conn, question, RERANK_CANDIDATES), k)


METHODS = {
    "vector": vector_search,
    "keyword": keyword_search,
    "hybrid": hybrid_search,
    "vector_rerank": vector_rerank_search,
    "hybrid_rerank": hybrid_rerank_search,
}


def retrieve(conn: psycopg.Connection, question: str, k: int = 5, method: str = "hybrid") -> list[Hit]:
    return METHODS[method](conn, question, k)
