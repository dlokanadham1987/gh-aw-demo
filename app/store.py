from datetime import datetime, timezone
from typing import Dict, List

from .models import Note, NoteIn


class NoteStore:
    """In-memory note store. Single-process only; resets on restart."""

    def __init__(self) -> None:
        self._notes: Dict[int, Note] = {}
        self._next_id: int = 1

    def add(self, data: NoteIn) -> Note:
        note = Note(
            id=self._next_id,
            title=data.title,
            body=data.body,
            created_at=datetime.now(timezone.utc),
        )
        self._notes[note.id] = note
        self._next_id += 1
        return note

    def get(self, note_id: int) -> Note | None:
        return self._notes.get(note_id)

    def list(self) -> List[Note]:
        return sorted(self._notes.values(), key=lambda n: n.id)


store = NoteStore()
