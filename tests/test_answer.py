from tutor.answer import build_context, check_citations, label
from tutor.retrieve import Hit


def hit(section_number, section_title, subsection, content):
    return Hit(1, "m1", section_number, section_title, subsection, "text", content, 0.0)


def test_label_with_and_without_subsection():
    assert label(hit("5.2", "Newton's First Law", "Gravitation and Inertia", "")) == \
        "§5.2 Newton's First Law › Gravitation and Inertia"
    assert label(hit(None, "Introduction", None, "")) == "Introduction"


def test_context_numbers_passages_from_one():
    context = build_context([hit("5.2", "Newton's First Law", None, "A body at rest..."),
                             hit("6.2", "Friction", None, "Friction opposes...")])
    assert context.startswith("[1] §5.2 Newton's First Law\nA body at rest...")
    assert "\n\n[2] §6.2 Friction\nFriction opposes..." in context


def test_citations_in_first_use_order_including_lists():
    cited, invalid = check_citations("Inertia [2]. Mass matters [1, 3]. Again [2].", 5)
    assert cited == [2, 1, 3]
    assert invalid == []


def test_citations_outside_the_passages_are_flagged():
    cited, invalid = check_citations("Claim [1]. Made up [7].", 5)
    assert cited == [1, 7]
    assert invalid == [7]
