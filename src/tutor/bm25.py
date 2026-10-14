"""BM25 keyword ranking, written out by hand.

Each chunk is one "document". For a question, every question word that
appears in a chunk adds IDF × (saturated TF):

  IDF  = ln((N - df + 0.5) / (df + 0.5) + 1)     rare words count more
  TF   = tf(k1 + 1) / (tf + k1(1 - b + b·|D|/avgdl))

Unlike Postgres's ts_rank_cd, IDF uses corpus-wide counts, so a word that
appears in many chunks ("back", "starts") matters little.

The index lives in memory: a few thousand chunks build in about a second, and
it can't go stale when the chunking changes.
"""

import math
import re
from collections import Counter

K1 = 1.2   # saturation: how fast extra repeats of a word stop adding score
B = 0.75   # length normalization: 0 = ignore chunk length, 1 = fully normalize

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "do", "does", "for", "from", "how",
    "i", "if", "in", "is", "it", "its", "my", "of", "on", "or", "so", "that", "the",
    "this", "to", "was", "what", "when", "where", "which", "why", "with",
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in STOP_WORDS]


class BM25Index:
    def __init__(self, texts: list[str]):
        docs = [tokenize(t) for t in texts]
        self.term_counts = [Counter(d) for d in docs]   # TF per chunk
        self.lengths = [len(d) for d in docs]
        self.avgdl = sum(self.lengths) / len(docs) if docs else 0.0
        n = len(docs)
        df = Counter(word for counts in self.term_counts for word in counts)
        self.idf = {w: math.log((n - f + 0.5) / (f + 0.5) + 1) for w, f in df.items()}

    def score(self, question: str) -> list[float]:
        words = [w for w in tokenize(question) if w in self.idf]
        scores = []
        for counts, length in zip(self.term_counts, self.lengths, strict=True):
            norm = K1 * (1 - B + B * length / self.avgdl)
            scores.append(sum(
                self.idf[w] * counts[w] * (K1 + 1) / (counts[w] + norm)
                for w in words if counts[w]
            ))
        return scores

    def top_k(self, question: str, k: int) -> list[tuple[int, float]]:
        """(position in corpus, score), best first; chunks with no matching word are left out."""
        ranked = sorted(enumerate(self.score(question)), key=lambda pair: pair[1], reverse=True)
        return [(i, s) for i, s in ranked[:k] if s > 0]
