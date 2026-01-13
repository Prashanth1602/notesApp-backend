from sqlalchemy.orm import Session
from models.notes import Notes
from sqlalchemy import func
from utils.logger import setup_logger

logger = setup_logger("search_utils")

def search_notes(db: Session, query: str, user_id: int):
    if query:
        terms = query.strip().split()
        if terms:
            logger.info(f"Searching notes for user_id: {user_id} with query: '{query}'")
            ts_query = " & ".join(f"{term}:*" for term in terms)
            results = db.query(Notes).filter(
                Notes.user_id == user_id,
                Notes.search_vector.op("@@")(func.to_tsquery("english", ts_query))
            ).all()
            logger.info(f"Found {len(results)} results for query: '{query}'")
            return results
    return []
