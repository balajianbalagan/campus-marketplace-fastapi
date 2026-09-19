from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()

SECRET_KEY = "exercise-secret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# {username: {"hashed_password": ..., "role": ...}}
USERS: dict[str, dict] = {}


class RegisterIn(BaseModel):
    username: str
    password: str
    role: str = "member"


# TODO: pwd_context.hash(plain)
def hash_password(plain: str) -> str:
    raise NotImplementedError


# TODO: pwd_context.verify(plain, hashed)
def verify_password(plain: str, hashed: str) -> bool:
    raise NotImplementedError


# TODO: jwt.encode({"sub": username, "exp": datetime.utcnow() + timedelta(minutes=60)}, SECRET_KEY, algorithm=ALGORITHM)
def create_token(username: str) -> str:
    raise NotImplementedError


@app.post("/register", status_code=201)
def register(payload: RegisterIn):
    # TODO: 400 if payload.username in USERS. Otherwise store
    # USERS[payload.username] = {"hashed_password": hash_password(payload.password), "role": payload.role}
    # and return {"username": payload.username, "role": payload.role}.
    raise NotImplementedError


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    # TODO: look up USERS.get(form.username); 401 (same message) if missing or
    # verify_password(form.password, user["hashed_password"]) is False. Otherwise return
    # {"access_token": create_token(form.username), "token_type": "bearer"}.
    raise NotImplementedError


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    # TODO: decode the token (401 on JWTError or missing "sub"), look up USERS[username]
    # (401 if missing), return {"username": username, **USERS[username]}.
    raise NotImplementedError


def require_officer(user: dict = Depends(get_current_user)) -> dict:
    # TODO: 403 if user["role"] != "officer", else return user.
    raise NotImplementedError


@app.delete("/club-funds/{amount}")
def spend_funds(amount: int, user: dict = Depends(require_officer)):
    return {"approved_by": user["username"], "amount": amount}
