"""Turn text into vectors with a local embedding model (a bi-encoder).

Passages and queries are embedded separately, so every chunk's vector is
computed once at ingest time and only the question is embedded per search.
"""

from functools import lru_cache

import numpy as np

from tutor.config import EMBEDDING_MODEL, QUERY_INSTRUCTION


@lru_cache(maxsize=1)
def get_model():
    # Imported here so modules that only need passage_text() stay fast to load.
    from sentence_transformers import SentenceTransformer

    # Use the cached copy without asking the Hugging Face Hub (a slow network
    # check that can take minutes); download only the first time.
    try:
        return SentenceTransformer(EMBEDDING_MODEL, local_files_only=True)
    except OSError:
        return SentenceTransformer(EMBEDDING_MODEL)


def passage_text(
    chapter_number: int,
    chapter_title: str,
    section_number: str | None,
    section_title: str,
    subsection_title: str | None,
    content: str,
) -> str:
    """The text we embed for a chunk: its heading path, then the chunk itself.

    The heading path tells the model where a short paragraph lives, e.g.
    "Ch 5 Newton's Laws of Motion › 5.2 Newton's First Law › Gravitation and Inertia".
    """
    section = f"{section_number} {section_title}" if section_number else section_title
    path = [f"Ch {chapter_number} {chapter_title}", section]
    if subsection_title:
        path.append(subsection_title)
    return " › ".join(path) + "\n\n" + content


def embed_passages(texts: list[str], batch_size: int = 64) -> np.ndarray:
    # normalize -> every vector has length 1, so cosine similarity = dot product
    return get_model().encode(
        texts, batch_size=batch_size, normalize_embeddings=True, show_progress_bar=True
    )


def embed_query(question: str) -> np.ndarray:
    return get_model().encode(QUERY_INSTRUCTION + question, normalize_embeddings=True)


def token_count(text: str) -> int:
    return len(get_model().tokenizer(text)["input_ids"])
