from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from db.database import Base


class PasswordRequestsStatus(enum.Enum):
    valid = 1
    expired = 2


class PasswordRequestsModel(Base):
    __tablename__ = "password_requests"

    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=datetime.now())
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    due_date = Column(DateTime)
    view_counter = Column(Integer, default=0)
    status = Column(Enum(PasswordRequestsStatus), default=PasswordRequestsStatus.valid)
    password_id = relationship("PasswordModel", uselist=False, back_populates="password_parent")


class PasswordModel(Base):
    __tablename__ = "password"

    id = Column(Integer, primary_key=True)
    password = Column(String)
    password_requests_id = Column(Integer, ForeignKey('password_requests.id'))
    password_parent = relationship("PasswordRequestsModel", back_populates="password_id")


class PasswordRequestsIn(BaseModel):
    user_id: int
    due_date: Optional[datetime] = None
    view_counter: int
    status: Optional[enum.Enum] = None


class PasswordRequestsOut(BaseModel):
    public_id: str
    due_date: Optional[datetime] = None
    view_counter: int
    status: Optional[enum.Enum] = None

