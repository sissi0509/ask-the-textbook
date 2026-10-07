from pathlib import Path

import pytest

from tutor.ingest.chunking import parse_module

MODULE = Path(__file__).parent / "fixtures" / "mini_book" / "modules" / "b2"


@pytest.fixture
def module():
    return parse_module(MODULE)


def texts(module):
    return [c.content for c in module.chunks if c.chunk_type == "text"]


def test_paragraph_before_any_subsection_has_no_subsection(module):
    first = module.chunks[0]
    assert first.subsection_title is None
    assert first.content.startswith("Experience suggests")


def test_figure_link_leaves_no_empty_parentheses(module):
    assert "()" not in module.chunks[0].content


def test_key_idea_box_keeps_its_title(module):
    assert "Newton's First Law of Motion: A body at rest" in texts(module)[1]


def test_equation_and_continuation_join_the_paragraph(module):
    joined = [t for t in texts(module) if t.startswith("We can give")]
    expected = (
        "We can give Newton's first law in vector form for any object we study: "
        "F_net = 0 so the velocity is constant."
    )
    assert joined == [expected]


def test_list_joins_its_paragraph(module):
    listed = next(t for t in texts(module) if "parked car" in t)
    assert listed.endswith("- weight\n- the normal force")


def test_subsection_title_is_recorded(module):
    assert module.chunks[2].subsection_title == "Newton's First Law and Equilibrium"


def test_skipped_parts_never_become_chunks(module):
    everything = " ".join(c.content for c in module.chunks)
    for skipped in ["Learning objectives", "hockey puck", "your car", "skydiver",
                    "simulation", "cupcake", "net force is needed"]:
        assert skipped not in everything


def test_summary_is_returned_separately(module):
    assert module.summary == "- A net force is needed to change motion.\n- Inertia resists changes in motion."


def test_glossary_becomes_definition_chunks(module):
    definitions = [c for c in module.chunks if c.chunk_type == "definition"]
    assert [d.content for d in definitions] == ["inertia: ability of an object to resist changes in its motion"]


def test_positions_are_sequential(module):
    assert [c.position for c in module.chunks] == list(range(len(module.chunks)))
