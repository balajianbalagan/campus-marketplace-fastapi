from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_session
from app.models import User, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


# TODO(module-5): POST /auth/register
# - 400 if username is already taken
# - hash the password, save a new User, return it
# - response_model=UserRead, status_code=201
@router.post("/register")
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    raise NotImplementedError("TODO: implement register")


# TODO(module-5): POST /auth/login
# - form: OAuth2PasswordRequestForm = Depends()
# - 401 with the SAME message for "no such user" and "wrong password"
# - return {"access_token": ..., "token_type": "bearer"}
@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    raise NotImplementedError("TODO: implement login")
