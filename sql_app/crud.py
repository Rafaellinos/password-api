from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import random
import string
import secrets

from pydantic import BaseModel
from . import models, schemas

SECRET_KEY = "afe99645a1078d18524d735a0915f354ed09db42443003938b32b200c802dc4a"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_user(db: Session, user: schemas.UserIn):
    db_user = models.User(username=user.username, password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username, "is_active": db_user.is_active}


def generate_random_key(key_size: int = 12) -> str:
    # secretes implements HRNG
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(key_size))


def create_password(user: int, db: Session, password_request: schemas.PasswordRequestsIn):
    password = models.Password(
        password=generate_random_key(),
    )
    password_request = models.PasswordRequests(
        user_id=user,
        due_date=password_request.due_date,
        view_counter=password_request.view_counter,
        status=password_request.status,
        password_id=password,
    )
    db.add_all([password, password_request])
    db.commit()
    db.refresh(password_request)
    return {
        "message": "Password Created!",
        "password_generated": password_request.public_id,
    }


def get_requests(user: int, db: Session) -> List[dict]:
    results = db.query(models.PasswordRequests).filter(models.PasswordRequests.user_id == user).all()
    return [
        {
            "public_id": getattr(r.public_id, "hex", ""),
            "due_date": r.due_date,
            "view_counter": r.view_counter,
            "status": r.status,
        }
        for r in results
    ]


def get_request(user: int, db: Session, public_id: str) -> dict:
    result = db.query(models.PasswordRequests).filter(
        models.PasswordRequests.public_id == public_id and \
        models.PasswordRequests.user_id == user).first()
    return {
        "public_id": getattr(result.public_id, "hex", ""),
        "due_date": result.due_date,
        "view_counter": result.view_counter,
        "status": result.status,
    }


def request_password(user: int, db: Session, public_id: str) -> dict:
    result = db.query(models.PasswordRequests).filter(
        models.PasswordRequests.public_id == public_id and \
        models.PasswordRequests.user_id == user
    ).first()

    if not result.view_counter or datetime.now() > result.due_date:
        result.status = models.PasswordRequestsStatus.expired
        db.commit()

    if result.status == models.PasswordRequestsStatus.expired:
        if result.password_id:
            db.delete(result.password_id)
            db.commit()
        return {
            "message": "Sorry, your password is expired",
        }

    result.view_counter -= 1
    db.commit()
    return {
        "password": result.password_id.password,
        "view_counter": result.view_counter,
        "due_date": result.due_date,
    }

