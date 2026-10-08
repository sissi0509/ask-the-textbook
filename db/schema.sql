-- Applied by the code on every run (safe to repeat). init.sql only runs once.
-- See docs/SCHEMA.md for a diagram and what every column means.

-- One row per section of the book. The book's structure never changes,
-- so this table is independent of how we chunk the text.
CREATE TABLE IF NOT EXISTS sections (
    id              TEXT PRIMARY KEY,      -- OpenStax module id, e.g. 'm58295'
    volume          INTEGER NOT NULL,
    unit_title      TEXT NOT NULL,         -- e.g. 'Mechanics'
    chapter_number  INTEGER NOT NULL,
    chapter_title   TEXT NOT NULL,
    section_number  TEXT,                  -- '5.1'; NULL for a chapter introduction
    section_title   TEXT NOT NULL,
    book_position   INTEGER NOT NULL,      -- order within the volume, 1-based
    UNIQUE (volume, book_position)
);

-- The section's own summary (one per section), filled by the chunk loader.
ALTER TABLE sections ADD COLUMN IF NOT EXISTS summary TEXT;

-- The searchable pieces of text. Rebuilt whenever the chunking strategy changes.
CREATE TABLE IF NOT EXISTS chunks (
    id                BIGSERIAL PRIMARY KEY,
    section_id        TEXT NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
    position          INTEGER NOT NULL,    -- order within the section, 0-based
    subsection_title  TEXT,                -- NULL before the first subsection
    chunk_type        TEXT NOT NULL CHECK (chunk_type IN ('text', 'definition')),
    content           TEXT NOT NULL,       -- what the LLM reads
    embedding         vector(384),         -- filled in T3
    UNIQUE (section_id, position)
);

-- Keyword search (Postgres full-text): kept in sync automatically from the text.
ALTER TABLE chunks ADD COLUMN IF NOT EXISTS search_vector tsvector
    GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(subsection_title, '') || ' ' || content)
    ) STORED;
CREATE INDEX IF NOT EXISTS chunks_search_vector_idx ON chunks USING GIN (search_vector);

-- Extra embedding models for the model comparison (evals/compare_models.py).
-- The app's default model stays in chunks.embedding. The vector has no fixed
-- size because models differ (384 vs 768); fine without an ANN index.
CREATE TABLE IF NOT EXISTS chunk_embeddings (
    chunk_id   BIGINT NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
    model      TEXT NOT NULL,                  -- Hugging Face model name
    embedding  vector NOT NULL,
    PRIMARY KEY (chunk_id, model)
);
