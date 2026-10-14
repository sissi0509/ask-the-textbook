# T-BM25: Add a true BM25 keyword path and compare it to Postgres full-text

## Goal

Add `bm25` and `hybrid_bm25_rerank` as retrieval methods, run the retrieval eval, and answer one question: **does IDF fix the keyword collisions** ("gun kick **back**" → "**back** emf", "bus **starts**" → electric motors) that made hybrid lose to `vector_rerank` at 3-volume scale?

## Hypothesis

`ts_rank_cd` has no IDF, so common words like "back" and "starts" count as much as "centripetal". BM25 down-weights words that appear in many chunks. If the hypothesis holds, `hybrid_bm25_rerank` should match or beat `vector_rerank` (98% Recall@5 on Vol. 1 questions), and the keyword-only row should rise above 73%.

## Before coding (look first)

- **The corpus = the rows of `chunks`** from all 3 volumes, kept as **separate chunks**. Each chunk is one BM25 "document" (document = the unit you rank). DF = how many chunks contain a word. Don't glue the text into one giant document: every word would get DF = 1, so IDF would be the same for all words, and there'd be only one score, so nothing to rank.
- **Index the same text as the full-text column:** `subsection_title + ' ' + content` (see `db/schema.sql:34`). Same input means the comparison is about the *scoring*, not the text.
- **Count the chunks first** (`SELECT count(*) FROM chunks`). It's a few thousand, so an in-memory index in plain Python is fine. No new database extension.
- **No new library.** BM25 is about 30 lines of Python with `collections.Counter` and `math.log`. Writing it yourself is the point: you'll know every term in the formula. (`rank_bm25` exists; skip it unless you get stuck.)

## The formula you'll implement

For a question with words q₁…qₙ and a chunk D:

```
score(D) = Σ over question words q:  IDF(q) × tf·(k1+1) / (tf + k1·(1 − b + b·|D|/avgdl))

IDF(q) = ln( (N − df + 0.5) / (df + 0.5) + 1 )
```

- `tf` = times q appears in D; `df` = chunks containing q; `N` = number of chunks
- `|D|` = words in D; `avgdl` = average words per chunk
- `k1 = 1.2` (saturation), `b = 0.75` (length normalization)

## Files

### `src/tutor/bm25.py` (new): BM25 only, no database
- **What it does:** builds an index from a list of texts and scores a question against it.
- **What's inside:**
  - `K1 = 1.2`, `B = 0.75` constants, with a one-line comment on what each controls.
  - `tokenize(text) -> list[str]`: lowercase, split on non-letters/digits, drop a small stop-word set ("the", "a", "of", "is", …). No stemming in the first version (MVP); note it as the next rep.
  - `BM25Index`: a dataclass built once from `list[str]`. Stores: per-chunk term counts (`list[Counter]`), per-chunk lengths, `avgdl`, `N`, and an `idf: dict[str, float]` computed at build time.
  - `BM25Index.score(question) -> list[float]`: one score per chunk, in corpus order.
  - `BM25Index.top_k(question, k) -> list[tuple[int, float]]`: (position in corpus, score), best first, skipping zero scores.
- **Why separate from `retrieve.py`:** pure math, testable without Postgres. `retrieve.py` stays about SQL + fusion.

### `src/tutor/retrieve.py` (edit)
- `bm25_search(conn, question, k) -> list[Hit]`:
  - On the first call, load `id` + indexed text for every chunk (same columns as `COLUMNS`, ordered by `id`) and build the `BM25Index`. Cache both in a module-level variable so later calls don't reload.
  - `top_k` → map corpus positions back to chunk ids → `Hit`s with the BM25 score.
- `hybrid_bm25_search`: `rrf_merge([vector_search(...CANDIDATES), bm25_search(...CANDIDATES)], k)`, the same shape as `hybrid_search`.
- `hybrid_bm25_rerank_search`: `rerank(question, hybrid_bm25_search(..., RERANK_CANDIDATES), k)`.
- Add all three to `METHODS` as `bm25`, `hybrid_bm25`, `hybrid_bm25_rerank`. Leave `DEFAULT_METHOD` alone until the eval says otherwise.
- Update the module docstring's method list.

### `tests/test_bm25.py` (new)
Use a 3-document toy corpus you can compute by hand, e.g.
`["centripetal force circle", "force force force push", "the bus starts moving"]`.
- **IDF:** a word in 1 of 3 docs gets a higher IDF than a word in 2 of 3 docs.
- **Rare beats repeated:** for "centripetal force", doc 0 outranks doc 1 even though doc 1 says "force" three times.
- **Saturation:** going from tf 1 → 2 adds more score than going from tf 2 → 3.
- **Length normalization:** the same single match scores higher in a short doc than in a long doc padded with unrelated words.
- **No match:** a question with only unknown words gets all-zero scores; `top_k` returns `[]`.
- **tokenize:** lowercases, drops stop words and punctuation.
- One hand-computed value: write out IDF and the score for one (question, doc) pair on paper, then assert it with `pytest.approx`.

## Evaluate

```
uv run python evals/run_retrieval_eval.py --methods keyword bm25 vector_rerank hybrid_rerank hybrid_bm25_rerank
```

- **Compare rows:** `keyword` vs. `bm25` (does IDF help alone?), and `hybrid_rerank` vs. `hybrid_bm25_rerank` vs. `vector_rerank` (does it fix fusion?).
- **Check the collision cases by hand:** print `bm25` top 5 for "gun kick back" and "bus starts". Is "back emf" gone from the top?
- **Record the result** in `docs/DESIGN.md` (new section after the 3-volume results) and the metrics table in `notes/PROJECT_NOTES.md`, even if BM25 loses. A negative result is still an interview story.

## Done when

- `uv run pytest` passes, including `tests/test_bm25.py`.
- `uv run ruff check` is clean.
- A dated report is in `evals/results/`, and DESIGN.md says whether BM25 earned a place in the default pipeline.

## Next reps (not this task)

- Stemming (try a tiny suffix stripper, or NLTK's Porter stemmer if needed) so "forces" matches "force".
- Rerank the **union** of vector top 30 + BM25 top 10 instead of the RRF top 30 (the fix idea already in DESIGN.md).
- Tune `k1`/`b` only if there's a clear reason; the defaults usually work.
