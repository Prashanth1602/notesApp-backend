from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from schemas.users import UserSchema, UserCreate, UserLogin
from schemas.auth import TokenResponse
from models.users import Users
from db_config import get_db 
from utils.auth import verify_password, get_password_hash, authenticate_user
from utils.token import get_current_user_from_token, create_access_token, refresh_access_token

router = APIRouter()

@router.post('/logout')
def logout(response: Response, current_user: Users = Depends(get_current_user_from_token)):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}

@router.post('/login')
def login(user_credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        access_token, refresh_token = authenticate_user(user_credentials.email, user_credentials.password, db)
    except ValueError as e:
         raise HTTPException(status_code=401, detail="Incorrect email or password")

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60
    )
    return {"access_token": access_token, "token_type": "bearer"}

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

@router.post("/refresh", response_model=TokenResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    print(f"DEBUG: Cookies received: {request.cookies.keys()}", flush=True)
    refresh_token = request.cookies.get("refresh_token")
    print(f"DEBUG: Refresh token received: {'Yes' if refresh_token else 'No'}", flush=True)
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    try:
        access_token, new_refresh_token = refresh_access_token(db, refresh_token_str=refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60
    )
    return {"access_token": access_token}