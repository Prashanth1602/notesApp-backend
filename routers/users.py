from fastapi import APIRouter
from sqlalchemy.orm import Session
from schemas.users import UserSchema, UserCreate, UserLogin, UserUpdate
from models import Users, Notes
from db_config import get_db
from fastapi import APIRouter, Depends, HTTPException
from utils.auth import create_token, verify_password, get_password_hash, get_current_user_from_token

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

@router.post('/logout')
def logout(current_user: Users = Depends(get_current_user_from_token)):
    return {"message": "Logged out successfully"}

@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    token = create_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.post('/register', response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter((Users.email == user.email) | (Users.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email or Username already registered")
        
    hashed_password = get_password_hash(user.password)
    new_user = Users(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
