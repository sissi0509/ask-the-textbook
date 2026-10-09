import json

import pytest
from fastapi.testclient import TestClient

from tutor import api
from tutor.answer import Answer, Retry
from tutor.retrieve import Hit


@pytest.fixture
def client(monkeypatch):
    # No models, database, or API calls in tests: replace them with fakes.
    monkeypatch.setattr(api.embeddings, "get_model", lambda: None)
    monkeypatch.setattr(api.rerank, "get_model", lambda: None)
    monkeypatch.setattr(api, "connect", FakeConnection)
    hit = Hit(1, "m58296", "5.2", "Newton's First Law", None, "text", "A body at rest...", 0.9)
    answer = Answer("Inertia [1].", [hit], [1], [], 100, 50, 0.0014, grounded=True)
    monkeypatch.setattr(api, "stream_answer", lambda conn, q, method: iter(["Iner", "tia [1].", answer]))
    monkeypatch.setattr(api, "stream_direct_answer", lambda q: iter(["From memory.", answer]))
    with TestClient(api.app) as test_client:
        yield test_client


class FakeConnection:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def events(response):
    return [json.loads(line) for line in response.text.splitlines()]


def test_ask_streams_text_then_the_finished_answer(client):
    lines = events(client.post("/ask", json={"question": "Why do I lean back?"}))
    assert [e["type"] for e in lines] == ["text", "text", "done"]
    assert "".join(e["text"] for e in lines[:2]) == "Inertia [1]."
    done = lines[-1]["answer"]
    assert done["sources"] == [{"n": 1, "label": "Vol. 1 §5.2 Newton's First Law", "ref": "1:5.2"}]
    assert done["passages"][0]["content"] == "A body at rest..."
    assert done["grounded"] is True and done["attempts"] == 1


def test_a_failed_citation_check_streams_a_retry_event(client, monkeypatch):
    hit = Hit(1, "m58296", "5.2", "Newton's First Law", None, "text", "A body at rest...", 0.9)
    answer = Answer("Inertia [1].", [hit], [1], [], 200, 100, 0.0028, grounded=True, attempts=2)
    monkeypatch.setattr(api, "stream_answer", lambda conn, q, method: iter(
        ["Uncited.", Retry("it cites no passages"), "Inertia [1].", answer]))
    lines = events(client.post("/ask", json={"question": "Why do I lean back?"}))
    assert [e["type"] for e in lines] == ["text", "retry", "text", "done"]
    assert lines[1] == {"type": "retry", "reason": "it cites no passages"}
    assert lines[-1]["answer"]["attempts"] == 2


def test_direct_answer_has_no_retrieval_step(client):
    lines = events(client.post("/ask/direct", json={"question": "What is inertia?"}))
    assert lines[0] == {"type": "text", "text": "From memory."}


def test_empty_question_is_rejected(client):
    assert client.post("/ask", json={"question": ""}).status_code == 422


def test_errors_during_the_stream_are_reported_in_band(client, monkeypatch):
    def failing(conn, q, method):
        yield "Partial"
        raise RuntimeError("The model declined to answer this question.")

    monkeypatch.setattr(api, "stream_answer", failing)
    lines = events(client.post("/ask", json={"question": "x"}))
    assert lines[-1] == {"type": "error", "message": "The model declined to answer this question."}


def test_cors_allows_the_frontend_origin(client):
    response = client.options("/ask", headers={"Origin": "http://localhost:3100",
                                               "Access-Control-Request-Method": "POST"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:3100"
