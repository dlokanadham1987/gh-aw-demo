from fastapi import FastAPI, HTTPException

from .models import Note, NoteIn
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


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int) -> Note:
    note = store.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="note not found")
    return note
