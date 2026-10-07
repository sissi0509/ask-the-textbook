# T1: Build the `sections` table from the book's structure

## Goal

Read Volume 1's structure from the downloaded OpenStax files, store one row per section in a new `sections` table, and print the chapter → section tree.

## Before coding (look at the files first)

- `data/openstax-physics/META-INF/books.xml`: three `<book>` entries. Each has a `slug` (e.g. `university-physics-volume-1`) and an `href` pointing to its collection file.
- `collections/university-physics-volume-1.collection.xml`: the order of everything. The nesting is **unit → chapter → modules**. Vol 1 has 2 units (Mechanics; Waves and Acoustics) and 17 chapters.
- **Front and back matter sit outside any chapter:** `m62204` (Preface) is at the top, and 7 appendix modules are at the bottom. They aren't sections; skip them.
- **Numbering isn't in the files.** The first module of every chapter is its Introduction, which gets no section number. The modules after it are 1, 2, 3… Chapter numbers keep counting across units: Mechanics ends at Ch 14, so Oscillations is Ch 15.
- **Module titles aren't in the collection.** Each module's title is the first `<title>` in `modules/<id>/index.cnxml`.
- **XML namespaces:** these files declare namespaces (`http://cnx.rice.edu/cnxml`, `.../collxml`, `.../mdml`). Python's built-in `xml.etree.ElementTree` writes tags with the namespace in braces, like `{http://cnx.rice.edu/collxml}module`. Searching for plain `module` finds nothing. Try it once in a Python shell before writing the parser.
- No new libraries are needed: `xml.etree.ElementTree` (built in) and `psycopg` (already installed).

## Files

### `db/schema.sql`
- **What it does:** creates the `sections` table if it doesn't exist.
- **What's inside:** `id` (module id, primary key), `volume`, `unit_title`, `chapter_number`, `chapter_title`, `section_number` (text, NULL for introductions), `section_title`, `book_position` (order within the volume). Unique on `(volume, book_position)`.
- **Why `section_number` is text:** as a number, "5.10" would equal "5.1".
- **Why separate from `init.sql`:** `init.sql` runs only once, when the volume is first created. `schema.sql` is applied by your code on every run, so you can change it and re-run. `CREATE TABLE IF NOT EXISTS` keeps it safe to repeat.

### `src/tutor/config.py`
- **What it does:** one place for settings.
- **What's inside:** loads `.env`; `DATABASE_URL`; `BOOK_DIR` (path to `data/openstax-physics`).
- **Why a separate file:** every later task needs the same settings.

### `src/tutor/db.py`
- **What it does:** database helpers.
- **What's inside:** `connect()` returns a connection using `DATABASE_URL`; `apply_schema(conn)` runs `db/schema.sql`.

### `src/tutor/ingest/structure.py`: parsing only, no database
- **What it does:** turns the XML files into Python objects.
- **What's inside:**
  - `Section`: a dataclass with the same fields as the table.
  - `find_collection(book_dir, volume) -> Path`: reads `books.xml`, returns the path to that volume's collection file.
  - `read_module_title(module_dir) -> str`
  - `parse_collection(collection_path, modules_dir, volume) -> list[Section]`: walks units → chapters → modules in order, skips modules outside chapters, assigns chapter numbers, section numbers, and `book_position`.
- **Why separate from loading:** pure functions with no database are easy to test, including in CI, which has no database and no book.

### `src/tutor/ingest/load_sections.py`
- **What it does:** the script you run.
- **What's inside:** `main()`: find the collection → parse → `apply_schema` → **upsert** the rows (`INSERT … ON CONFLICT (id) DO UPDATE`, the same pattern as your SigIQ report store) → print the tree. Run it as `uv run python -m tutor.ingest.load_sections`.
- **Why upsert:** running it twice must not create duplicates.

### `tests/fixtures/mini_book/`
- A tiny fake book with the same layout as the real one: a `books.xml`, one collection with a preface module, 2 units, 3 chapters (2 modules each, the first titled "Introduction"), an appendix module, and the matching `modules/<id>/index.cnxml` files containing only a `<title>`.
- **Why:** tests can't use `data/`, which isn't in git, so CI doesn't have it. A fixture you control also lets you test edge cases on purpose.

### `tests/test_structure.py`: what each test checks
- `find_collection` returns the right file for volume 1.
- `read_module_title` returns the module's title.
- Preface and appendix modules are **not** in the result.
- Introductions have `section_number = None`; the next module in the chapter is `"<chapter>.1"`.
- Chapter numbers **continue across units** (the first chapter of unit 2 is Ch 3, not Ch 1).
- `book_position` runs 1, 2, 3… with no gaps.

## Done when

- `uv run pytest` passes locally, and CI is green.
- Running `load_sections` prints **17 chapters** and **116 sections** (17 introductions + 99 numbered), starting `Ch 1 Units and Measurement`, and `Ch 15` is Oscillations.
- Running it a second time still leaves 116 rows.
- TablePlus shows the `sections` table with sensible values. Spot-check §5.1 = "Forces" (`m58295`).
