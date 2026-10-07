"""Split one module (section) into chunks, and pull out its summary.

v1 rules (see docs/DESIGN.md):
  - each paragraph -> a 'text' chunk
  - a display equation or a bullet list joins the paragraph before it
    ("We can write the law in vector form:" + the equation)
  - so does a paragraph that continues a derivation ("so v_T = mg/b."):
    one that starts in lowercase or has fewer than MIN_WORDS words
  - key-idea boxes ("Newton's First Law of Motion: ...") and problem-solving
    boxes -> a 'text' chunk, title included
  - glossary entries -> 'definition' chunks ("inertia: ability of an object ...")
  - the Summary subsection -> returned separately (stored on the section)
  - skipped for now: worked examples, figures, tables, check-your-understanding,
    simulations, conceptual questions, problems, key-equation lists
"""

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from tutor.ingest.mathml import MATHML, math_to_text

CNX = "{http://cnx.rice.edu/cnxml}"

SUMMARY_CLASS = "key-concepts"
SKIPPED_SECTION_CLASSES = {
    "key-equations",
    "review-conceptual-questions",
    "review-problems",
    "review-additional-problems",
    "review-challenge",
}
KEPT_NOTE_CLASSES = {None, "problem-solving"}  # None = a key-idea box
JOIN_NOTE_CLASS = "equation-callout"           # an equation set off in a box
MIN_WORDS = 8


@dataclass
class Chunk:
    position: int
    subsection_title: str | None
    chunk_type: str
    content: str


@dataclass
class ModuleText:
    chunks: list[Chunk]
    summary: str | None


def _tag(e: ET.Element) -> str:
    return e.tag.replace(CNX, "")


def text_of(e: ET.Element) -> str:
    """All text inside an element, with math converted to readable text."""
    parts = [e.text or ""]
    for child in e:
        if child.tag == f"{MATHML}math":
            parts.append(f" {math_to_text(child)} ")
        else:
            parts.append(text_of(child))
        parts.append(child.tail or "")
    return "".join(parts)


def clean(text: str) -> str:
    text = " ".join(text.split())
    text = re.sub(r"\(\s*\)", "", text)            # "(Figure 5.3)" links leave "()" behind
    text = re.sub(r"\s+([.,;:!?)])", r"\1", text)  # no space before punctuation
    text = re.sub(r"\(\s+", "(", text)
    return " ".join(text.split())


def _continues_previous(text: str) -> bool:
    return bool(text) and (text[0].islower() or len(text.split()) < MIN_WORDS)


def _box_text(note: ET.Element) -> str:
    title = clean(note.findtext(f"{CNX}title") or "")
    body = " ".join(clean(text_of(k)) for k in note if _tag(k) != "title")
    return f"{title}: {body}" if title else body


def _list_text(lst: ET.Element) -> str:
    return "\n".join(f"- {clean(text_of(item))}" for item in lst if _tag(item) == "item")


class _Builder:
    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self.summary: str | None = None

    def add(self, subsection: str | None, chunk_type: str, content: str) -> None:
        if content:
            self.chunks.append(Chunk(len(self.chunks), subsection, chunk_type, content))

    def join_to_previous(self, subsection: str | None, content: str, sep: str = " ") -> None:
        """Attach an equation or list to the paragraph it belongs to."""
        last = self.chunks[-1] if self.chunks else None
        if last and last.chunk_type == "text" and last.subsection_title == subsection:
            last.content = f"{last.content}{sep}{content}" if content else last.content
        else:
            self.add(subsection, "text", content)

    def walk(self, container: ET.Element, subsection: str | None) -> None:
        for child in container:
            tag = _tag(child)
            if tag == "section":
                cls = child.get("class")
                if cls == SUMMARY_CLASS:
                    self.summary = "\n".join(
                        _list_text(k) if _tag(k) == "list" else clean(text_of(k))
                        for k in child if _tag(k) in ("list", "para")
                    ) or None
                elif cls not in SKIPPED_SECTION_CLASSES:
                    title = clean(child.findtext(f"{CNX}title") or "") or subsection
                    self.walk(child, title)
            elif tag == "para":
                text = clean(text_of(child))
                if _continues_previous(text):
                    self.join_to_previous(subsection, text)
                else:
                    self.add(subsection, "text", text)
            elif tag == "equation":
                self.join_to_previous(subsection, clean(text_of(child)))
            elif tag == "list":
                self.join_to_previous(subsection, _list_text(child), sep="\n")
            elif tag == "note":
                cls = child.get("class")
                if cls == JOIN_NOTE_CLASS:
                    self.join_to_previous(subsection, clean(text_of(child)))
                elif cls in KEPT_NOTE_CLASSES:
                    self.add(subsection, "text", _box_text(child))
            # example, figure, table, exercise, media, title: skipped in v1


def parse_module(module_dir: Path) -> ModuleText:
    document = ET.parse(module_dir / "index.cnxml").getroot()
    builder = _Builder()
    builder.walk(document.find(f"{CNX}content"), None)

    glossary = document.find(f"{CNX}glossary")
    if glossary is not None:
        for definition in glossary.findall(f"{CNX}definition"):
            term = clean(text_of(definition.find(f"{CNX}term")))
            meaning = clean(text_of(definition.find(f"{CNX}meaning")))
            builder.add("Glossary", "definition", f"{term}: {meaning}")

    return ModuleText(builder.chunks, builder.summary)
