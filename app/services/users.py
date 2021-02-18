import logging
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.services.errors import NotFound
from app.models.users import UserModel, UserIn, UserPassword
from app.config.settings import get_settings


logger = logging.getLogger("uvicorn.error")
settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    try:
        return db.query(UserModel).filter(UserModel.username == username).first()
    except:
        logger.warning("user not found %s" % username)
        raise NotFound


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    try:
        if not verify_password(password, user.password):
            return False
    except UnknownHashError as err:
        logger.error(str(err))
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    return encoded_jwt


def create_user(db: Session, user: UserIn) -> dict:
    try:
        db_user = UserModel(username=user.username, password=get_password_hash(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info("user created %s" % db_user.public_id)
    except Exception as e:
        logger.error(str(e))
    return {
        "username": db_user.username,
        "is_active": db_user.is_active,
    }


def update_password(db: Session, user_id: int, new_password: UserPassword) -> dict:
    user = db.query(UserModel).filter(
        UserModel.id == user_id and \
        UserModel.is_active
    ).first()
    user.password = get_password_hash(new_password.password)
    db.commit()
    return {
        "message": "password updated",
    }
