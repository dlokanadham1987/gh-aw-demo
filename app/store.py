import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from pydantic import ValidationError

from .models import Note, NoteIn, NoteUpdate

logger = logging.getLogger(__name__)


class NoteStore:
    """In-memory note store. Single-process only; resets on restart.

    On init, attempts to load `app/seed.json` so the API always has dummy data
    after a fresh start. The seed file is optional — missing or malformed seed
    is treated as "start empty" without raising.
    """

    def __init__(self) -> None:
        self._notes: Dict[int, Note] = {}
        self._next_id: int = 1
        self._load_seed()

    def _load_seed(self) -> None:
        seed_path = Path(__file__).parent / "seed.json"
        if not seed_path.exists():
            return
        try:
            with open(seed_path, encoding="utf-8") as f:
                seed_data = json.load(f)
            for item in seed_data:
                self.add(NoteIn(title=item["title"], body=item.get("body", "")))
        except (json.JSONDecodeError, KeyError, OSError, TypeError, ValidationError) as e:
            logger.warning("failed to load seed.json: %s", e)

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

    def update(self, note_id: int, data: NoteUpdate) -> Note | None:
        note = self._notes.get(note_id)
        if note is None:
            return None
        updates = data.model_dump(exclude_unset=True, exclude_none=True)
        if not updates:
            return note
        updated = note.model_copy(update=updates)
        self._notes[note_id] = updated
        return updated


store = NoteStore()
