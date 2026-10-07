"""Second-stage reranking with a cross-encoder.

A bi-encoder (embeddings.py) turns question and passage into vectors
separately, which is fast but approximate. A cross-encoder reads the question
and one passage *together* and outputs one relevance score, which is much
more precise but too slow to run on every chunk. So it only re-sorts the
first stage's short list.
"""

from functools import lru_cache

from tutor.config import RERANK_MODEL


@lru_cache(maxsize=1)
def get_model():
    from sentence_transformers import CrossEncoder

    # Use the cached copy without asking the Hugging Face Hub (a slow network
    # check that can take minutes); download only the first time.
    try:
        return CrossEncoder(RERANK_MODEL, local_files_only=True)
    except OSError:
        return CrossEncoder(RERANK_MODEL)


def rerank_scores(question: str, passages: list[str]) -> list[float]:
    return get_model().predict([(question, p) for p in passages]).tolist()
