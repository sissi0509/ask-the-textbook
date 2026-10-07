"""Read the book's structure (units, chapters, sections) from the OpenStax files.

Parsing only: no database here, so it's easy to test.

The OpenStax source has three layers:
  META-INF/books.xml       which collection file belongs to which volume
  collections/*.xml        the order: unit -> chapter -> module ids
  modules/<id>/index.cnxml one section's content, including its title

Section numbers aren't stored anywhere. Each chapter's first module is its
Introduction (no number); the next ones are <chapter>.1, <chapter>.2, ...
Modules outside any chapter (preface, appendices) are not sections.
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

# Every tag in these files lives in an XML namespace, so ElementTree names
# tags like "{http://cnx.rice.edu/collxml}module". These prefixes let us
# write "col:module" in searches instead.
NS = {
    "container": "https://openstax.org/namespaces/book-container",
    "col": "http://cnx.rice.edu/collxml",
    "md": "http://cnx.rice.edu/mdml",
    "cnx": "http://cnx.rice.edu/cnxml",
}


@dataclass
class Section:
    id: str
    volume: int
    unit_title: str
    chapter_number: int
    chapter_title: str
    section_number: str | None
    section_title: str
    book_position: int


def find_collection(book_dir: Path, volume: int) -> Path:
    """Return the collection file for a volume, using META-INF/books.xml."""
    books = ET.parse(book_dir / "META-INF" / "books.xml").getroot()
    for book in books.findall("container:book", NS):
        if book.get("slug", "").endswith(f"-volume-{volume}"):
            return (book_dir / "META-INF" / book.get("href")).resolve()
    raise ValueError(f"Volume {volume} not found in books.xml")


def read_module_title(module_dir: Path) -> str:
    """A module's title is the first <title> directly under <document>."""
    document = ET.parse(module_dir / "index.cnxml").getroot()
    return document.findtext("cnx:title", namespaces=NS).strip()


def parse_collection(collection_path: Path, modules_dir: Path, volume: int) -> list[Section]:
    """Walk unit -> chapter -> modules in book order and number everything."""
    root = ET.parse(collection_path).getroot()
    sections: list[Section] = []
    chapter_number = 0

    # Only subcollections are units; modules directly under the root
    # (preface, appendices) are skipped by not looking at them.
    for unit in root.find("col:content", NS).findall("col:subcollection", NS):
        unit_title = unit.findtext("md:title", namespaces=NS)
        for chapter in unit.find("col:content", NS).findall("col:subcollection", NS):
            chapter_number += 1
            chapter_title = chapter.findtext("md:title", namespaces=NS)
            modules = chapter.find("col:content", NS).findall("col:module", NS)
            for index, module in enumerate(modules):
                module_id = module.get("document")
                sections.append(
                    Section(
                        id=module_id,
                        volume=volume,
                        unit_title=unit_title,
                        chapter_number=chapter_number,
                        chapter_title=chapter_title,
                        # index 0 is the chapter's Introduction
                        section_number=f"{chapter_number}.{index}" if index > 0 else None,
                        section_title=read_module_title(modules_dir / module_id),
                        book_position=len(sections) + 1,
                    )
                )
    return sections
