import os
import bcrypt
from models.auth import Users, RefreshToken
from datetime import datetime, timedelta
from utils.token import create_access_token, create_refresh_token
from sqlalchemy.orm import Session
from fastapi import Depends
from db_config import get_db

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Incorrect email or password")
    access_token = create_access_token(user)
    refresh_token = create_refresh_token()

    refresh_token_entry = RefreshToken(
        token = refresh_token,
        user_id = user.id,
        expires_at = datetime.utcnow() + timedelta(days=7)
    )
    db.add(refresh_token_entry)
    db.commit()  
    return access_token, refresh_token  