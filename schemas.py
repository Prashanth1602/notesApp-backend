from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class NoteSchema(BaseModel):
    id: int
    title: str
    content: str
    is_archived: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str
    content: str

class NoteDelete(BaseModel):
    id: int

