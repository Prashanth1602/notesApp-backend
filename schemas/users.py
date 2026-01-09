from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str
    email: str

class UserDelete(BaseModel):
    id: int

class UserLogin(BaseModel):
    email: str
    password: str

class UserLogout(BaseModel):
    id: int
    token: str