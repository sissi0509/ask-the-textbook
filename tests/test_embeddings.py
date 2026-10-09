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


class FakeModel:
    """Stands in for a SentenceTransformer: records what it was asked to encode."""

    def __init__(self):
        self.seen = []

    def encode(self, text, normalize_embeddings):
        self.seen.append(text)
        return [0.0]


def test_query_prefix_depends_on_the_model(monkeypatch):
    import tutor.embeddings as emb
    from tutor.config import QUERY_INSTRUCTION

    fake = FakeModel()
    monkeypatch.setattr(emb, "get_model", lambda model=emb.EMBEDDING_MODEL: fake)

    emb.embed_query("Why do I lean back?")  # default bge-small wants the instruction
    emb.embed_query("Why do I lean back?", model="sentence-transformers/all-MiniLM-L6-v2")

    assert fake.seen == [QUERY_INSTRUCTION + "Why do I lean back?", "Why do I lean back?"]
