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
