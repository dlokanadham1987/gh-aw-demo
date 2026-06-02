from datetime import datetime
from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    body: str = Field(default="", max_length=4000)


class Note(NoteIn):
    id: int
    created_at: datetime
