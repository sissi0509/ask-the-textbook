import json
from pathlib import Path

import pytest

from tutor.topics import TOPICS, topic_of

CASES = Path(__file__).parents[1] / "evals" / "retrieval_cases.jsonl"


def test_topic_follows_volume_and_chapter():
    assert topic_of("1:5.2") == "Mechanics"
    assert topic_of("1:14.1") == "Mechanics"
    assert topic_of("1:15.1") == "Oscillations & Waves"
    assert topic_of("2:4.3") == "Thermodynamics"
    assert topic_of("2:5.1") == "Electricity & Magnetism"
    assert topic_of("3:4.1") == "Optics"
    assert topic_of("3:5.2") == "Modern Physics"


def test_unknown_chapter_is_an_error():
    with pytest.raises(ValueError):
        topic_of("1:18.1")


def test_every_eval_case_has_the_topic_of_its_gold_section():
    for line in CASES.read_text().splitlines():
        case = json.loads(line)
        assert case["topic"] in TOPICS
        assert case["topic"] == topic_of(case["gold"][0]), case["id"]
