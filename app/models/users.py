from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Optional
from pydantic import BaseModel
import uuid

from db.database import Base
from models.requests import PasswordRequestsModel


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    password_requests_ids = relationship("PasswordRequestsModel")


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
