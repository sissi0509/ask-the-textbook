# Design decisions

Short record of decisions and why. Newest at the bottom.

## Data source

OpenStax *University Physics* (CC BY-NC-SA 4.0), from the CNXML source repo, downloaded with a sparse checkout into `data/` (gitignored). Only `META-INF/`, `collections/`, `modules/` are fetched; `media/` (images, ~200 MB) is skipped in v1. v1 uses Volume 1.

- `collections/*.collection.xml` gives the book's order: unit → chapter → module ids. It has no section numbers and no module titles.
- `modules/<id>/index.cnxml` holds one section: titles, paragraphs, equations (MathML), examples, definitions, notes, figures, exercises.
- Section numbers are derived from position: the first module of each chapter is the Introduction (no number), then 1, 2, …

## Two tables: `sections` and `chunks`

- **`sections`**: one row per module: volume, unit, chapter number/title, section number/title, position in the book. It describes the book's structure, which never changes.
- **`chunks`**: the searchable units, each pointing to its section (`section_id`). Chunking strategies will change and get compared; the book's structure won't. Keeping them separate means re-chunking never touches `sections`.

Also: T1 can fill `sections` before any chunking exists; eval gold labels point to real section ids; per-section data (e.g. links) is stored once.

## One `chunks` table for all chunk types

All searchable text lives in `chunks` with a `chunk_type` column, so one hybrid query (vector + full-text + RRF) searches everything, and `WHERE chunk_type = ...` filters by type. Full column reference: [SCHEMA.md](SCHEMA.md).

## v1 chunking rules (T2)

v1 keeps only prose (paragraphs + definitions). Worked examples and figures can be added later as new chunk types without changing the pipeline.

- **Paragraph = chunk** (`text`). A display equation or a bullet list joins the paragraph before it. So does a paragraph that continues a derivation (starts lowercase or has under 8 words, e.g. "so v_T = mg/b.").
- **Math** is converted from MathML to readable text (`F⃗_net = 0⃗`).
- **Key-idea and problem-solving boxes** → `text`, title included ("Newton's First Law of Motion: A body at rest…").
- **Glossary** → `definition` chunks ("inertia: ability of an object to resist changes in its motion").
- **Subsection titles** → a `subsection_title` column on each chunk, not a separate table: nothing uses subsections on their own.
- **Summary** → `sections.summary` (one per section). Planned v2 ablation: search summaries first to find the section, then its chunks (hierarchical retrieval).
- **Skipped in v1:** worked examples, figures, tables, check-your-understanding, simulations, conceptual questions, problems, key-equation lists.

Volume 1 result: 116 sections → 1,970 chunks (1,649 text, 321 definitions); text chunks have a median of 68 words. 99 summaries (introductions have none).

**Known limitation:** a few chunks are long (max ~900 words, mostly long bullet lists). Measured with the model's tokenizer in T3: **3 of 1,970 chunks** exceed the 512-token limit, so their endings are cut off when embedded.

**Future option, from review: natural blocks vs. strategy chunks.** Split the current table in two: `blocks` (the book's natural paragraphs, fixed) and `chunks` (built from blocks by a chunking strategy, with a `strategy` column; long blocks split, small ones merged). That would let several strategies sit side by side for the chunking ablation. Not needed yet: re-parsing takes seconds and re-embedding about 25 s, so strategies can be compared one after another.

## Embeddings (T3)

- **Model:** `BAAI/bge-small-en-v1.5`, local and free, 384 dimensions, reads up to 512 tokens. It's a **bi-encoder**: passages and questions are embedded separately, so each chunk's vector is computed once at ingest.
- **What gets embedded:** the heading path + the chunk, e.g. `Ch 5 Newton's Laws of Motion › 5.2 Newton's First Law › Gravitation and Inertia` + the paragraph, so short paragraphs carry their context. The stored `content` stays clean for the LLM.
- **Queries** get the model's retrieval prefix (`Represent this sentence for searching relevant passages: `); passages don't.
- **Vectors are normalized** (length 1), so cosine similarity is just a dot product.
- **No vector index yet:** at ~2,000 rows an exact scan is fast and always correct (no approximate-index recall loss, no over-filtering).
- **Speed:** all of Volume 1 embeds in **~24 s** on a laptop CPU (~80 chunks/s).

**First retrieval smoke test (vector only):**
- "Why does a spinning skater speed up when she pulls her arms in?" → top 3 all from §11.3 Conservation of Angular Momentum ✅
- "What is inertia?" → the §5.2 glossary definition first ✅
- "Why do I lean back when the bus suddenly starts?" → §11.4 gyroscopes, §6.3 centripetal force ❌ (should be §5.2 inertia). Everyday wording vs. textbook wording: exactly the gap keyword search, HyDE, and reranking should close. It's the first case for the eval set.

## Retrieval and the first ablation (T4)

Three methods in `tutor/retrieve.py`, each adding one layer:
- **vector**: cosine distance on the bge embeddings (exact scan).
- **keyword**: Postgres full-text search on a generated `search_vector` column (GIN index). The question's words are OR-ed (`plainto_tsquery` ANDs them, so a natural question would match almost nothing) and ranked with `ts_rank_cd`. BM25-like, but with no collection-wide IDF.
- **hybrid**: top 50 from each path, merged with **Reciprocal Rank Fusion** (score = Σ 1/(60 + rank)). It uses ranks because the two scores are on different scales.

**Eval set** (`evals/retrieval_cases.jsonl`): 42 questions, 14 each of *textbook* wording, *everyday* wording, and exact *terms*, each with gold section(s). Hit = any retrieved chunk from a gold section. Drafted by Claude with gold sections checked against the chunks. Still to do: Xi's review and misconception-style cases.

**First results (2026-10-06):**

| Method | Recall@5 | Recall@10 | MRR | R@5 everyday | R@5 term | R@5 textbook |
|---|---|---|---|---|---|---|
| vector | 90% | 95% | 0.90 | 71% | 100% | 100% |
| keyword | 81% | 86% | 0.57 | 57% | 100% | 86% |
| hybrid | 93% | 93% | 0.89 | 86% | 100% | 93% |

Reading it:
- **Hybrid helps everyday questions** (71% → 86%): keyword matches like "siren"/"ambulance" and "skydiver" rescue cases the vectors missed.
- **But it adds noise at the top:** MRR doesn't improve, and one textbook question (#3 "How is linear momentum defined?") drops out of the top 5 because keyword search ranks chapter introductions that repeat "momentum". That's the job a cross-encoder reranker is for.
- **Still missed by everything:** the bus/inertia question (#15) and the guitar-beats question (#23). Both are everyday wording with no shared keywords, which is the case HyDE targets.
- **Caveats:** 42 cases, so one case = 2.4 points. Term questions are at 100% for every method (too easy, a ceiling effect). The set needs harder cases before small differences mean anything.

## Reranking (second stage)

Before building it, we checked the reranker's **ceiling**: a reranker can only re-sort candidates it's given. Hybrid's **Recall@20 was 100%**: every gold section was in the top 20, and the three misses sat at ranks 15, 16, and 20. So a reranker over the top 30 could, in principle, fix all of them.

- **Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2` (small, local). It reads *question + passage together* and outputs one relevance score.
- **Input:** `section title › subsection` + the chunk text, for the top **30** first-stage candidates.

| Method | Recall@5 | Recall@10 | MRR | R@5 everyday | R@5 term | R@5 textbook | Latency (median) |
|---|---|---|---|---|---|---|---|
| vector | 90% | 95% | 0.90 | 71% | 100% | 100% | 31 ms |
| keyword | 81% | 86% | 0.57 | 57% | 100% | 86% | |
| hybrid | 93% | 93% | 0.89 | 86% | 100% | 93% | 27 ms |
| vector + rerank | 95% | 95% | 0.95 | 86% | 100% | 100% | |
| **hybrid + rerank** | **95%** | **98%** | **0.95** | 86% | 100% | **100%** | 576 ms |

Reading it:
- **The reranker did its job, cleaning the top of the list:** MRR 0.89 → 0.95, and the textbook question that keyword noise had pushed down (#3, linear momentum) is back in the top 5.
- **Cost:** about +0.55 s per question on a laptop CPU, which is fine for a tutor. It's the price of running a model 30 times per question.
- **Still missed:** #15 (bus → inertia) and #23 (out-of-tune strings → beats). The reranker found nearby physics (friction, centripetal force, musical sound) but not the exact concept. Both are pure wording mismatches, the case HyDE is designed for.
- vector + rerank ≈ hybrid + rerank on Recall@5 here; hybrid + rerank wins Recall@10 (98%). With 42 cases these differences are 1 question; we'll keep hybrid + rerank as the default because the keyword path protects exact-term questions on a larger, harder set.

## Name and source (2026-10-07)

The project started as "Learn Physics with Feynman", hoping to use *The Feynman Lectures on Physics*. Permission was requested from the publisher; the editor of the New Millennium Edition replied that the rights don't allow AI use and the online edition is read-only. The project was renamed **Ask the Textbook** and is built only on OpenStax. The explanation style (intuition first, everyday examples) comes from the prompt, not from any copyrighted text.

## Answer generation (T5): v1 end to end

`uv run python -m tutor.cli "question"` → hybrid + rerank top 5 → Claude (`claude-opus-5-5`, effort `medium`) → streamed answer + sources + token cost (~$0.02 per question).

- **Style from the prompt:** intuition first, an everyday example, plain words before terms, then the precise statement; ~150–250 words; ends with a check-yourself question. No persona, no "Feynman".
- **Grounding rules:** physics facts only from the numbered passages; cite `[n]`; say plainly what the passages don't cover; never invent quotes.
- **Code owns the citations:** the model writes `[3]`; code maps it to `§6.3 Centripetal Force › Inertial Forces…` from the database and flags any number that wasn't a passage.
- **Thinking counts toward `max_tokens`:** set to 16,000 so it never cuts off the visible answer (learned in the contamination probe).

**First two answers:**
- *Bus question:* explained with a tablecloth analogy, quoted §6.3 word for word ("a physicist would say that you tend to remain stationary while the seat pushes forward on you"), and **named a gap** it couldn't fill from the passages.
- *Redshift (complex case #43):* explained the Doppler part from §17.7 and said clearly that the passages "never use the word 'redshift'" and "say nothing about relativity", exactly the honest behavior the case's note asked for.

**Eval correction found through T5:** the bus question's best passage was in **§6.3 Inertial Forces** (same example: pushed back into a jet seat), which the eval had counted as a miss. Gold is now §5.2 + §6.3. Re-run: hybrid + rerank **Recall@5 98%, Recall@10 100%, MRR 0.96**; the only miss left is #23 (guitar beats). Lesson: retrieval "misses" need reading before they're trusted, because gold labels can be too narrow.
