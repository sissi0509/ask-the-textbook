from types import SimpleNamespace

import pytest

from tutor import answer as answer_module
from tutor.answer import Answer, Retry, build_context, check_citations, citation_problem, label
from tutor.retrieve import Hit


def hit(section_number, section_title, subsection, content):
    return Hit(1, "m1", section_number, section_title, subsection, "text", content, 0.0)


def test_label_with_and_without_subsection():
    assert label(hit("5.2", "Newton's First Law", "Gravitation and Inertia", "")) == \
        "Vol. 1 §5.2 Newton's First Law › Gravitation and Inertia"
    intro = hit(None, "Introduction", None, "")
    intro.chapter_number = 5
    assert label(intro) == "Vol. 1 Ch. 5 Introduction"


def test_context_numbers_passages_from_one():
    context = build_context([hit("5.2", "Newton's First Law", None, "A body at rest..."),
                             hit("6.2", "Friction", None, "Friction opposes...")])
    assert context.startswith("[1] Vol. 1 §5.2 Newton's First Law\nA body at rest...")
    assert "\n\n[2] Vol. 1 §6.2 Friction\nFriction opposes..." in context


def test_citations_in_first_use_order_including_lists():
    cited, invalid = check_citations("Inertia [2]. Mass matters [1, 3]. Again [2].", 5)
    assert cited == [2, 1, 3]
    assert invalid == []


def test_citations_outside_the_passages_are_flagged():
    cited, invalid = check_citations("Claim [1]. Made up [7].", 5)
    assert cited == [1, 7]
    assert invalid == [7]


def test_citation_problem_passes_only_valid_cited_answers():
    assert citation_problem([1, 2], []) is None
    assert citation_problem([], []) == "it cites no passages"
    assert citation_problem([1, 7], [7]) == "it cites passages that don't exist (7)"


def fake_message(text):
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)],
                           usage=SimpleNamespace(input_tokens=100, output_tokens=50))


@pytest.fixture
def scripted(monkeypatch):
    """Make the model return the given answers in turn; record what it was sent."""
    calls = []

    def script(*texts):
        replies = iter(texts)

        def fake_stream(system, messages):
            calls.append(messages)
            text = next(replies)
            yield text
            yield fake_message(text)

        monkeypatch.setattr(answer_module, "_stream", fake_stream)
        passages = [hit("5.2", "Newton's First Law", None, "A body at rest..."),
                    hit("6.2", "Friction", None, "Friction opposes...")]
        monkeypatch.setattr(answer_module, "retrieve", lambda conn, q, k, method: passages)
        return calls

    return script


def run(question="Why do I lean back?"):
    return list(answer_module.stream_answer(None, question))


def test_a_cited_answer_passes_on_the_first_attempt(scripted):
    calls = scripted("Inertia [1].")
    pieces = run()
    assert not any(isinstance(p, Retry) for p in pieces)
    final = pieces[-1]
    assert isinstance(final, Answer)
    assert final.grounded and final.attempts == 1 and final.cited == [1]
    assert len(calls) == 1


def test_an_uncited_answer_is_retried_with_a_correction(scripted):
    calls = scripted("Inertia, from memory.", "Inertia [1].")
    pieces = run()
    assert pieces[1] == Retry("it cites no passages")
    final = pieces[-1]
    assert final.text == "Inertia [1]." and final.grounded and final.attempts == 2
    # The retry shows the model its first answer, then the correction.
    retry_messages = calls[1]
    assert retry_messages[1] == {"role": "assistant", "content": "Inertia, from memory."}
    assert "cites no passages" in retry_messages[2]["content"]
    # Usage adds up both attempts.
    assert final.input_tokens == 200 and final.output_tokens == 100


def test_an_answer_citing_a_missing_passage_is_retried(scripted):
    scripted("Inertia [9].", "Inertia [2].")
    pieces = run()
    assert pieces[1] == Retry("it cites passages that don't exist (9)")
    assert pieces[-1].grounded and pieces[-1].cited == [2]


def test_an_answer_that_fails_twice_is_flagged_not_grounded(scripted):
    calls = scripted("No citations.", "Still none.")
    final = run()[-1]
    assert final.text == "Still none."
    assert not final.grounded and final.attempts == 2
    assert len(calls) == 2  # one retry only, then stop
