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

from tutor.config import RERANK_CANDIDATES
from tutor.embeddings import embed_query
from tutor.rerank import rerank_scores

RRF_K = 60          # standard RRF constant: dampens the gap between rank 1 and rank 2
CANDIDATES = 50     # how many results each path contributes before fusion

COLUMNS = """
    c.id, c.section_id, s.section_number, s.section_title,
    c.subsection_title, c.chunk_type, c.content
"""
# score comes next in every SELECT; volume is selected last
VOLUME = ", s.volume"


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

    @property
    def ref(self) -> str:
        """Volume-qualified section, e.g. '1:5.2'. Section numbers repeat across volumes."""
        return f"{self.volume}:{self.section_number}"


def vector_search(conn: psycopg.Connection, question: str, k: int) -> list[Hit]:
    register_vector(conn)
    rows = conn.execute(
        f"""SELECT {COLUMNS}, 1 - (c.embedding <=> %(q)s) AS score{VOLUME}
            FROM chunks c JOIN sections s ON s.id = c.section_id
            ORDER BY c.embedding <=> %(q)s
            LIMIT %(k)s""",
        {"q": embed_query(question), "k": k},
    ).fetchall()
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


def rerank(question: str, candidates: list[Hit], k: int) -> list[Hit]:
    """Second stage: re-sort first-stage candidates by cross-encoder score."""
    if not candidates:
        return []
    passages = [
        " › ".join(filter(None, [h.section_title, h.subsection_title])) + "\n" + h.content
        for h in candidates
    ]
    scores = rerank_scores(question, passages)
    ranked = sorted(zip(candidates, scores, strict=True), key=lambda pair: pair[1], reverse=True)
    return [Hit(**{**hit.__dict__, "score": float(score)}) for hit, score in ranked[:k]]


def vector_rerank_search(conn: psycopg.Connection, question: str, k: int) -> list[Hit]:
    return rerank(question, vector_search(conn, question, RERANK_CANDIDATES), k)


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
