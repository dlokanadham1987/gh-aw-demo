from fastapi.testclient import TestClient

from app.main import app
from app.store import store


def setup_function(_):
    store._notes.clear()
    store._next_id = 1


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_and_get_note():
    r = client.post("/notes", json={"title": "First", "body": "hello"})
    assert r.status_code == 201
    note = r.json()
    assert note["id"] == 1
    assert note["title"] == "First"

    r = client.get(f"/notes/{note['id']}")
    assert r.status_code == 200
    assert r.json()["body"] == "hello"


def test_list_notes_sorted():
    client.post("/notes", json={"title": "A"})
    client.post("/notes", json={"title": "B"})
    r = client.get("/notes")
    assert r.status_code == 200
    titles = [n["title"] for n in r.json()]
    assert titles == ["A", "B"]


def test_get_missing_note_returns_404():
    r = client.get("/notes/999")
    assert r.status_code == 404


def test_search_notes_matches_title_case_insensitive():
    client.post("/notes", json={"title": "Buy milk"})
    client.post("/notes", json={"title": "Buy bread"})
    client.post("/notes", json={"title": "Call mom"})
    r = client.get("/notes/search?q=BUY")
    assert r.status_code == 200
    titles = [n["title"] for n in r.json()]
    assert sorted(titles) == ["Buy bread", "Buy milk"]


def test_patch_note_updates_title_only():
    created = client.post("/notes", json={"title": "Old", "body": "keep"}).json()
    r = client.patch(f"/notes/{created['id']}", json={"title": "New"})
    assert r.status_code == 200
    note = r.json()
    assert note["title"] == "New"
    assert note["body"] == "keep"


def test_patch_note_updates_body_only():
    created = client.post("/notes", json={"title": "Title", "body": "old body"}).json()
    r = client.patch(f"/notes/{created['id']}", json={"body": "new body"})
    assert r.status_code == 200
    note = r.json()
    assert note["title"] == "Title"
    assert note["body"] == "new body"


def test_patch_missing_note_returns_404():
    r = client.patch("/notes/999", json={"title": "x"})
    assert r.status_code == 404


def test_patch_note_rejects_empty_title():
    created = client.post("/notes", json={"title": "Original"}).json()
    r = client.patch(f"/notes/{created['id']}", json={"title": ""})
    assert r.status_code == 422
