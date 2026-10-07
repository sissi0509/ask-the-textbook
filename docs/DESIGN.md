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

v1 keeps only what the Feynman Lectures also have (long prose), so a future switch to that text needs a new parser, not a new pipeline.

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
