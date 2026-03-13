from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    created_at: datetime


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
