from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import NoteSchema, NoteCreate, NoteUpdate, NoteDelete
from models import Notes
from db_config import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def check_health():
    return {'health': 'ok'}

@app.get('/notes', response_model=List[NoteSchema])
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(Notes).all()
    return notes

@app.post('/notes', response_model=NoteSchema)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Notes(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get('/notes/{note_id}', response_model=NoteSchema)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Notes).filter(Notes.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put('/notes/{note_id}', response_model=NoteSchema)
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(Notes).filter(Notes.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db_note.title = note_update.title
    db_note.content = note_update.content
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete('/notes/{note_id}')
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Notes).filter(Notes.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(db_note)
    db.commit()
    return {'message': 'Note deleted'}
