from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from schemas.users import UserSchema, UserCreate, UserUpdate
from models.users import Users
from models.notes import Notes
from db_config import get_db
from utils.token import get_current_user_from_token

router = APIRouter()

@router.get('/me', response_model=UserSchema)
def get_current_user(current_user: Users = Depends(get_current_user_from_token)):
    return current_user

@router.put('/me', response_model=UserSchema)
def update_user_me(user_update: UserUpdate, current_user: Users = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(
        ((Users.email == user_update.email) | (Users.username == user_update.username)) & (Users.id != current_user.id)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")

    current_user.username = user_update.username
    current_user.email = user_update.email
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete('/me')
def delete_user_me(current_user: Users = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    db.query(Notes).filter(Notes.user_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}

