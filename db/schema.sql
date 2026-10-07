-- Applied by the code on every run (safe to repeat). init.sql only runs once.

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
