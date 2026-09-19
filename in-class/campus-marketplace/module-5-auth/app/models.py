from datetime import datetime
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class Role(str, Enum):
    student = "student"
    moderator = "moderator"
    admin = "admin"


# ---- Users ----------------------------------------------------------------

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str                       # never exposed on a response model
    role: Role = Field(default=Role.student)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    password: str                               # plaintext, only ever lives in the request


class UserRead(UserBase):
    id: int
    role: Role


# ---- Listings ---------------------------------------------------------------

class ListingBase(SQLModel):
    title: str = Field(min_length=3, max_length=80)
    description: str = ""
    price_cents: int = Field(ge=0)


class Listing(ListingBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    seller_id: int = Field(foreign_key="user.id")
    photo_url: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ListingCreate(ListingBase):
    pass


class ListingRead(ListingBase):
    id: int
    seller_id: int
    photo_url: str | None
    created_at: datetime


class ListingUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    price_cents: int | None = None
