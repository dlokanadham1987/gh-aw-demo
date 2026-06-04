from fastapi import FastAPI, HTTPException, Query

from .models import Note, NoteIn, NoteUpdate
from .store import store

app = FastAPI(title="Mini Notes API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/notes", response_model=Note, status_code=201)
def create_note(payload: NoteIn) -> Note:
    return store.add(payload)


@app.get("/notes", response_model=list[Note])
def list_notes() -> list[Note]:
    return store.list()


@app.get("/notes/search", response_model=list[Note])
def search_notes(
    q: str = Query(..., min_length=1, max_length=120),
) -> list[Note]:
    needle = q.lower()
    return [n for n in store.list() if needle in n.title.lower()]


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int) -> Note:
    note = store.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="note not found")
    return note


@app.patch("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, payload: NoteUpdate) -> Note:
    note = store.update(note_id, payload)
    if note is None:
        raise HTTPException(status_code=404, detail="note not found")
    return note
