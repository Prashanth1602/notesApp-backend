from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.notes import NoteSchema, NoteCreate, NoteUpdate
from models.notes import Notes
from models.users import Users
from db_config import get_db
from utils.token import get_current_user_from_token
from utils.logger import setup_logger

logger = setup_logger("notes_router")

router = APIRouter()

@router.get('/', response_model=List[NoteSchema])
def get_notes(db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    logger.info(f"Fetching notes for user_id: {current_user.id}")
    notes = db.query(Notes).filter(Notes.user_id == current_user.id).all()
    return notes

@router.post('/', response_model=NoteSchema)
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    logger.info(f"Creating note for user_id: {current_user.id} with title: {note.title}")
    db_note = Notes(title=note.title, content=note.content, user_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    logger.info(f"Note created successfully with id: {db_note.id}")
    return db_note

@router.get('/{note_id}', response_model=NoteSchema)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    logger.info(f"Fetching note_id: {note_id} for user_id: {current_user.id}")
    note = db.query(Notes).filter(Notes.id == note_id, Notes.user_id == current_user.id).first()
    if note is None:
        logger.warning(f"Note not found note_id: {note_id} user_id: {current_user.id}")
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put('/{note_id}', response_model=NoteSchema)
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    db_note = db.query(Notes).filter(Notes.id == note_id, Notes.user_id == current_user.id).first()
    if db_note is None:
        logger.warning(f"Failed to update. Note not found note_id: {note_id}")
        raise HTTPException(status_code=404, detail="Note not found")
    
    db_note.title = note_update.title
    db_note.content = note_update.content
    db.commit()
    logger.info(f"Note updated successfully note_id: {note_id}")
    db.refresh(db_note)
    return db_note

@router.put('/{note_id}/archive', response_model=NoteSchema)
def archive_note(note_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    db_note = db.query(Notes).filter(Notes.id == note_id, Notes.user_id == current_user.id).first()
    if db_note is None:
        logger.warning(f"Failed to archive. Note not found note_id: {note_id}")
        raise HTTPException(status_code=404, detail="Note not found")
    
    logger.info(f"Archiving note_id: {note_id}")
    db_note.is_archived = True
    db.commit()
    db.refresh(db_note)
    return db_note

@router.put('/{note_id}/unarchive', response_model=NoteSchema)
def unarchive_note(note_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    db_note = db.query(Notes).filter(Notes.id == note_id, Notes.user_id == current_user.id).first()
    if db_note is None:
        logger.warning(f"Failed to unarchive. Note not found note_id: {note_id}")
        raise HTTPException(status_code=404, detail="Note not found")
    
    logger.info(f"Unarchiving note_id: {note_id}")
    db_note.is_archived = False
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete('/{note_id}')
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    db_note = db.query(Notes).filter(Notes.id == note_id, Notes.user_id == current_user.id).first()
    if db_note is None:
        logger.warning(f"Failed to delete. Note not found note_id: {note_id}")
        raise HTTPException(status_code=404, detail="Note not found")
    
    logger.info(f"Deleting note_id: {note_id}")
    db.delete(db_note)
    db.commit()
    return {'message': 'Note deleted'}
