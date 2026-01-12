import jwt
import os
from models.auth import Users, RefreshToken
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db_config import get_db
import secrets

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(user: Users):
    payload = {
        'user_id': user.id,
        'type': 'access',
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)

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

def refresh_access_token(db : Session = Depends(get_db), refresh_token_str : str = None):
    if not refresh_token_str:
         raise HTTPException(status_code=401, detail="Missing refresh token")

    token_record = db.query(RefreshToken).filter(RefreshToken.token == refresh_token_str, RefreshToken.is_revoked == False).first()
    if token_record is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")

    token_record.is_revoked = True

    new_refresh_token_value = create_refresh_token()
    
    new_refresh_token = RefreshToken(
        token = new_refresh_token_value,
        user_id = token_record.user_id,
        expires_at = datetime.utcnow() + timedelta(days=7)
    )
    db.add(new_refresh_token)
    
    user = db.query(Users).filter(Users.id == token_record.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_access_token(user)
    db.commit()
    return access_token, new_refresh_token_value
    