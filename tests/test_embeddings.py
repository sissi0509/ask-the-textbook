from tutor.embeddings import passage_text


def test_heading_path_with_subsection():
    text = passage_text(5, "Newton's Laws of Motion", "5.2", "Newton's First Law",
                        "Gravitation and Inertia", "Mass is related to inertia.")
    assert text == (
        "Ch 5 Newton's Laws of Motion › 5.2 Newton's First Law › Gravitation and Inertia"
        "\n\nMass is related to inertia."
    )


def test_heading_path_for_introduction_without_subsection():
    text = passage_text(5, "Newton's Laws of Motion", None, "Introduction", None, "Why things move.")
    assert text == "Ch 5 Newton's Laws of Motion › Introduction\n\nWhy things move."
