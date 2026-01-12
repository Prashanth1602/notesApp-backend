from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.search import SearchResponse
from utils.search import search_notes
from db_config import get_db
from utils.token import get_current_user_from_token
from models.users import Users

router = APIRouter()

@router.get("/", response_model=SearchResponse)
def search(query: str, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    results = search_notes(db, query, current_user.id)
    return {"results": results}
