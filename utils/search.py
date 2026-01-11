from sqlalchemy.orm import Session
from models import Notes
from sqlalchemy import or_

def search_notes(db: Session, query: str, user_id: int):
    return db.query(Notes).filter(
        Notes.user_id == user_id,
        or_(
            Notes.title.ilike(f"%{query}%"),
            Notes.content.ilike(f"%{query}%")
        )
    ).all()
