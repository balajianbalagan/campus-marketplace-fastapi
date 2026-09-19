from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel

# --- given: unchanged from Module 1, plus a new reporter_id foreign key --------------------

class Role(str, Enum):
    resident = "resident"
    staff = "staff"
    admin = "admin"


class ComplaintBase(SQLModel):
    category: str
    description: str = Field(min_length=10)
    location: str


class Complaint(ComplaintBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str = Field(default="open")
    reporter_id: int = Field(foreign_key="user.id")
    photo_url: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintRead(ComplaintBase):
    id: int
    status: str
    reporter_id: int
    photo_url: str | None
    created_at: datetime


class ComplaintUpdate(SQLModel):
    description: str | None = None
    location: str | None = None
    status: str | None = None


# --- given: user model shapes, same four-class pattern as Campus Marketplace ---------------

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    role: Role = Field(default=Role.resident)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: Role
