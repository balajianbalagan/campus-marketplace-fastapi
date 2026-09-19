from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.database import get_session
from app.models import Role, User

SECRET_KEY = "civic-complaint-tracker-homework-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# TODO(module-5): hash a plaintext password with pwd_context. See Campus Marketplace's app/auth.py.
def hash_password(plain: str) -> str:
    raise NotImplementedError("TODO: implement hash_password")


# TODO(module-5): verify a plaintext password against a stored hash.
def verify_password(plain: str, hashed: str) -> bool:
    raise NotImplementedError("TODO: implement verify_password")


# TODO(module-5): build a JWT whose payload is {"sub": subject, "exp": <expiry>},
# signed with SECRET_KEY using ALGORITHM. Expiry should be ACCESS_TOKEN_EXPIRE_MINUTES from now.
def create_access_token(subject: str) -> str:
    raise NotImplementedError("TODO: implement create_access_token")


# TODO(module-5): dependency. Decode `token` (401 on any JWTError or missing "sub" claim),
# look up the matching User by username, 401 if no such user, otherwise return it.
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    raise NotImplementedError("TODO: implement get_current_user")


# TODO(module-5): dependency FACTORY. require_role(Role.staff, Role.admin) should return a
# dependency that 403s (via HTTPException) unless the current user's role is in `allowed`,
# and otherwise returns that user. Look at Campus Marketplace's require_role for the shape.
def require_role(*allowed: Role):
    def checker(user: User = Depends(get_current_user)) -> User:
        raise NotImplementedError("TODO: implement require_role's inner checker")

    return checker
