from pathlib import Path

import pytest

from tutor.ingest.structure import find_collection, parse_collection, read_module_title

MINI = Path(__file__).parent / "fixtures" / "mini_book"


@pytest.fixture
def sections():
    collection = find_collection(MINI, volume=1)
    return parse_collection(collection, MINI / "modules", volume=1)


def by_id(sections):
    return {s.id: s for s in sections}


def test_find_collection_picks_the_right_volume():
    assert find_collection(MINI, 1).name == "mini-volume-1.collection.xml"
    assert find_collection(MINI, 2).name == "mini-volume-2.collection.xml"


def test_find_collection_unknown_volume():
    with pytest.raises(ValueError):
        find_collection(MINI, 9)


def test_read_module_title():
    assert read_module_title(MINI / "modules" / "b2") == "Newton's First Law"


def test_front_and_back_matter_are_skipped(sections):
    ids = [s.id for s in sections]
    assert "p1" not in ids  # preface
    assert "z1" not in ids  # appendix
    assert ids == ["a1", "a2", "b1", "b2", "c1", "c2"]


def test_introductions_have_no_number(sections):
    s = by_id(sections)
    assert s["a1"].section_number is None
    assert s["a1"].section_title == "Introduction"
    assert s["a2"].section_number == "1.1"


def test_chapter_numbers_continue_across_units(sections):
    s = by_id(sections)
    assert s["c2"].unit_title == "Waves"
    assert s["c2"].chapter_number == 3  # not 1, even though it's a new unit
    assert s["c2"].section_number == "3.1"


def test_book_position_has_no_gaps(sections):
    assert [s.book_position for s in sections] == [1, 2, 3, 4, 5, 6]
