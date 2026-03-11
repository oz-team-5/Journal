from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    created_at: datetime


class UserResponse(BaseModel):
    username: str
    created_at: datetime


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
