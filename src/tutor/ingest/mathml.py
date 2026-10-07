"""Turn MathML (how OpenStax writes equations) into short readable text.

  <msub><mi>F</mi><mtext>net</mtext></msub>  ->  F_net
  <mfrac><mi>d</mi><mi>t</mi></mfrac>        ->  d/t

Good enough for an embedding model and an LLM to read; not a full renderer.
"""

import xml.etree.ElementTree as ET

MATHML = "{http://www.w3.org/1998/Math/MathML}"

# Operators that read better with spaces around them.
SPACED_OPERATORS = {"=", "+", "−", "-", "×", "·", "<", ">", "≤", "≥", "≈", "∝", "→", "⇒"}
VECTOR_ARROW = "⃗"  # combining arrow above: v⃗
HAT = "̂"           # combining circumflex: î


def _tag(e: ET.Element) -> str:
    return e.tag.replace(MATHML, "")


def _group(text: str) -> str:
    """Wrap multi-character pieces in parentheses so a/b and x^2 stay unambiguous."""
    text = text.strip()
    return text if len(text) <= 1 or text.isalnum() else f"({text})"


def to_text(e: ET.Element) -> str:
    tag = _tag(e)
    kids = list(e)

    if tag in ("mi", "mn", "mtext", "ms"):
        return (e.text or "").strip()
    if tag == "mo":
        op = (e.text or "").strip()
        return f" {op} " if op in SPACED_OPERATORS else op
    if tag == "mspace":
        return " "
    if tag == "annotation" or tag == "annotation-xml":
        return ""
    if tag == "semantics":
        return to_text(kids[0]) if kids else ""
    if tag == "msub" and len(kids) == 2:
        return f"{to_text(kids[0])}_{_group(to_text(kids[1]))}"
    if tag == "msup" and len(kids) == 2:
        return f"{to_text(kids[0])}^{_group(to_text(kids[1]))}"
    if tag == "msubsup" and len(kids) == 3:
        return f"{to_text(kids[0])}_{_group(to_text(kids[1]))}^{_group(to_text(kids[2]))}"
    if tag == "mfrac" and len(kids) == 2:
        return f"{_group(to_text(kids[0]))}/{_group(to_text(kids[1]))}"
    if tag == "msqrt":
        return f"sqrt({''.join(to_text(k) for k in kids)})"
    if tag == "mroot" and len(kids) == 2:
        return f"root({to_text(kids[0])}, {to_text(kids[1])})"
    if tag == "mover" and len(kids) == 2:
        base, over = to_text(kids[0]), to_text(kids[1]).strip()
        if over in ("→", "⇀", "⟶"):
            return base + VECTOR_ARROW
        if over in ("^", "ˆ"):
            return base + HAT
        return f"{base}^{_group(over)}"
    if tag in ("munder", "munderover") and kids:
        parts = [to_text(k) for k in kids]
        text = parts[0]
        if len(parts) > 1:
            text += f"_{_group(parts[1])}"
        if len(parts) > 2:
            text += f"^{_group(parts[2])}"
        return text + " "
    if tag == "mfenced":
        open_, close = e.get("open", "("), e.get("close", ")")
        return open_ + ", ".join(to_text(k) for k in kids) + close
    if tag == "mtable":
        return "; ".join(to_text(row) for row in kids)

    # math, mrow, mstyle, mpadded, mtr, mtd, ...: just join the children
    return "".join(to_text(k) for k in kids)


def math_to_text(math: ET.Element) -> str:
    return " ".join(to_text(math).split())
