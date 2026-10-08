"""Second-stage reranking with a cross-encoder.

A bi-encoder (embeddings.py) turns question and passage into vectors
separately, which is fast but approximate. A cross-encoder reads the question
and one passage *together* and outputs one relevance score, which is much
more precise but too slow to run on every chunk. So it only re-sorts the
first stage's short list.
"""

from functools import cache

from tutor.config import RERANK_MODEL


@cache
def get_model(model: str = RERANK_MODEL):
    from sentence_transformers import CrossEncoder

    # Use the cached copy without asking the Hugging Face Hub (a slow network
    # check that can take minutes); download only the first time.
    try:
        return CrossEncoder(model, local_files_only=True)
    except OSError:
        return CrossEncoder(model)


def rerank_scores(question: str, passages: list[str], model: str = RERANK_MODEL) -> list[float]:
    return get_model(model).predict([(question, p) for p in passages]).tolist()
