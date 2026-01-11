from pydantic import BaseModel
from typing import List
from schemas.notes import NoteSchema

class Search(BaseModel):
    query: str

class SearchResponse(BaseModel):
    results: List[NoteSchema]