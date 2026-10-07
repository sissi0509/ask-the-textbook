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

Text, worked examples, definitions, and summaries all live in `chunks` with a `chunk_type` column, so one hybrid query (vector + full-text + RRF) searches everything, and `WHERE chunk_type = ...` filters by type. Equations stay inline in their paragraph's text.

Not searchable in v1: check-your-understanding notes, conceptual questions, problems (saved aside as eval material), interactive media links. Figures: caption text only; image-to-text descriptions are a later feature.
