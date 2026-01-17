from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from utils.download import download_user_memories
from db_config import get_db
from models.users import Users
from utils.token import get_current_user_from_token

router = APIRouter()

@router.get("/")
def download_memories(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user_from_token)
):
    return StreamingResponse(
        download_user_memories(db, current_user.id),
        media_type="text/html",
        headers={
            "Content-Disposition": "attachment; filename=memories.html"
        },
    )

