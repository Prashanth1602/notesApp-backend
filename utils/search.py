from sqlalchemy.orm import Session
from models.notes import Notes
from sqlalchemy import func

def search_notes(db: Session, query: str, user_id: int):
    if query:
        terms = query.strip().split()
        if terms:
            ts_query = " & ".join(f"{term}:*" for term in terms)
            return db.query(Notes).filter(
                Notes.user_id == user_id,
                Notes.search_vector.op("@@")(func.to_tsquery("english", ts_query))
            ).all()
    return []
