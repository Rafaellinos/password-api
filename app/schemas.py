from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    is_active: Optional[bool] = None


class UserIn(User):
    password: str


class UserOut(User):
    public_id: str


class PasswordRequestsIn(BaseModel):
    user_id: int
    due_date: Optional[datetime] = None
    view_counter: int
    status: Optional[Enum] = None


class PasswordRequestsOut(BaseModel):
    public_id: str
    due_date: Optional[datetime] = None
    view_counter: int
    status: Optional[Enum] = None

