from tutor.retrieve import RRF_K, Hit, rrf_merge


def hit(chunk_id: int) -> Hit:
    return Hit(chunk_id, "m1", "1.1", "Title", None, "text", f"chunk {chunk_id}", 0.0)


def test_rrf_prefers_chunks_ranked_high_in_both_lists():
    vector = [hit(1), hit(2), hit(3)]
    keyword = [hit(3), hit(4), hit(1)]
    merged = rrf_merge([vector, keyword], k=4)
    # 1: ranks 1 and 3; 3: ranks 3 and 1 -> tied top; 2 and 4 appear once
    assert {h.chunk_id for h in merged[:2]} == {1, 3}
    assert merged[0].score == 1 / (RRF_K + 1) + 1 / (RRF_K + 3)


def test_rrf_keeps_chunks_found_by_only_one_list():
    merged = rrf_merge([[hit(1)], [hit(2)]], k=5)
    assert [h.chunk_id for h in merged] == [1, 2]


def test_rrf_respects_k():
    merged = rrf_merge([[hit(i) for i in range(10)]], k=3)
    assert len(merged) == 3


def test_rerank_reorders_by_cross_encoder_score(monkeypatch):
    import tutor.retrieve as retrieve_module

    # Fake cross-encoder: the passage mentioning "inertia" is most relevant.
    monkeypatch.setattr(
        retrieve_module, "rerank_scores",
        lambda question, passages, model: [1.0 if "inertia" in p else 0.0 for p in passages],
    )
    candidates = [hit(1), hit(2), Hit(3, "m1", "5.2", "Newton's First Law", None, "text",
                                     "inertia resists changes in motion", 0.0)]
    result = retrieve_module.rerank("Why do I lean back?", candidates, k=2)
    assert [h.chunk_id for h in result] == [3, 1]


def test_rerank_with_no_candidates():
    from tutor.retrieve import rerank

    assert rerank("anything", [], k=5) == []


def test_rerank_passes_the_model_name_through(monkeypatch):
    import tutor.retrieve as retrieve_module

    used = []
    monkeypatch.setattr(
        retrieve_module, "rerank_scores",
        lambda question, passages, model: used.append(model) or [0.0] * len(passages),
    )
    retrieve_module.rerank("q", [hit(1)], k=1, model="BAAI/bge-reranker-base")
    assert used == ["BAAI/bge-reranker-base"]


class FakeConn:
    """Records the SQL a search sends; returns no rows."""

    def __init__(self):
        self.sql, self.params = None, None

    def execute(self, sql, params):
        self.sql, self.params = sql, params
        return self

    def fetchall(self):
        return []


def test_vector_search_reads_extra_models_from_chunk_embeddings(monkeypatch):
    import tutor.retrieve as retrieve_module

    monkeypatch.setattr(retrieve_module, "register_vector", lambda conn: None)
    monkeypatch.setattr(retrieve_module, "embed_query", lambda question, model: [0.0])

    default, other = FakeConn(), FakeConn()
    retrieve_module.vector_search(default, "q", 5)
    retrieve_module.vector_search(other, "q", 5, embedding_model="BAAI/bge-base-en-v1.5")

    assert "chunk_embeddings" not in default.sql  # the app's default path is unchanged
    assert "chunk_embeddings" in other.sql
    assert other.params["model"] == "BAAI/bge-base-en-v1.5"
