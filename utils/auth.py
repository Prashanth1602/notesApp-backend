import jwt
import os
import bcrypt
from models import Users
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db_config import get_db

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def create_token(user: Users):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
    