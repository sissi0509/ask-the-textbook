import math

import pytest

from tutor.bm25 import K1, B, BM25Index, tokenize

# Small enough to check by hand: 3 chunks, average length 10/3 words.
TOY = ["centripetal force circle", "force force force push", "the bus starts moving"]


def test_tokenize_lowercases_and_drops_stop_words_and_punctuation():
    assert tokenize("The Centripetal force, of a circle!") == ["centripetal", "force", "circle"]


def test_rare_words_get_a_higher_idf():
    index = BM25Index(TOY)
    # "centripetal" is in 1 of 3 chunks, "force" in 2 of 3
    assert index.idf["centripetal"] > index.idf["force"]


def test_one_rare_word_beats_many_common_ones():
    scores = BM25Index(TOY).score("centripetal force")
    assert scores[0] > scores[1] > scores[2] == 0.0


def test_hand_computed_score():
    # IDF = ln((N - df + 0.5) / (df + 0.5) + 1), TF part = tf(k1+1) / (tf + k1(1 - b + b|D|/avgdl))
    avgdl = 10 / 3
    idf_force = math.log((3 - 2 + 0.5) / (2 + 0.5) + 1)
    tf_part = 3 * (K1 + 1) / (3 + K1 * (1 - B + B * 4 / avgdl))
    assert BM25Index(TOY).score("force")[1] == pytest.approx(idf_force * tf_part)


def test_repeats_saturate():
    # Same chunk length every time (3 words), so only tf changes.
    chunks = ["force pad pad", "force force pad", "force force force"]
    gains = [BM25Index([chunk, "other words here"]).score("force")[0] for chunk in chunks]
    assert gains[1] - gains[0] > gains[2] - gains[1]


def test_long_chunks_are_penalized():
    index = BM25Index(["force circle", "force circle push pull drag lift spin roll", "other"])
    scores = index.score("force")
    assert scores[0] > scores[1]


def test_unknown_words_score_zero_and_top_k_is_empty():
    index = BM25Index(TOY)
    assert index.score("quantum entanglement") == [0.0, 0.0, 0.0]
    assert index.top_k("quantum entanglement", 5) == []


def test_top_k_returns_best_positions_first_and_respects_k():
    result = BM25Index(TOY).top_k("centripetal force", 1)
    assert [position for position, _ in result] == [0]
