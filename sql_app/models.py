from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base
import enum
import uuid


class PasswordRequestsStatus(enum.Enum):
    valid = 1
    expired = 2


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    password_requests_ids = relationship("PasswordRequests")


class PasswordRequests(Base):
    __tablename__ = "password_requests"

    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=datetime.now())
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    due_date = Column(DateTime)
    view_counter = Column(Integer, default=0)
    status = Column(Enum(PasswordRequestsStatus), default=PasswordRequestsStatus.valid)
    password_id = relationship("Password", uselist=False, back_populates="password_parent")


class Password(Base):
    __tablename__ = "password"

    id = Column(Integer, primary_key=True)
    password = Column(String)
    password_requests_id = Column(Integer, ForeignKey('password_requests.id'))
    password_parent = relationship("PasswordRequests", back_populates="password_id")
