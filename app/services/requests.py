import string
import secrets
import logging
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from app.services.errors import NotFound
from app.models.requests import (
    PasswordModel,
    PasswordRequestsIn,
    PasswordRequestsModel,
    PasswordRequestsStatus,
)

logger = logging.getLogger("uvicorn.error")


def generate_random_key(key_size: int = 12) -> str:
    # secretes implements HRNG
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(key_size))


def create_password(user: int, db: Session, password_request: PasswordRequestsIn):
    password = PasswordModel(
        password=generate_random_key(),
    )
    password_request = PasswordRequestsModel(
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
    results = db.query(PasswordRequestsModel).filter(PasswordRequestsModel.user_id == user).all()
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
    try:
        result = db.query(PasswordRequestsModel).filter(
            PasswordRequestsModel.public_id == public_id and \
            PasswordRequestsModel.user_id == user).first()
    except:
        logger.error("request not found %s" % public_id)
        raise NotFound
    return {
        "public_id": getattr(result.public_id, "hex", ""),
        "due_date": result.due_date,
        "view_counter": result.view_counter,
        "status": result.status,
    }


def request_password(user: int, db: Session, public_id: str) -> dict:
    try:
        result = db.query(PasswordRequestsModel).filter(
            PasswordRequestsModel.public_id == public_id and \
            PasswordRequestsModel.user_id == user
        ).first()
    except:
        logger.error("password request not found %s" % public_id)
        raise NotFound

    if not result.view_counter or datetime.now() > result.due_date:
        result.status = PasswordRequestsStatus.expired
        db.commit()

    if result.status == PasswordRequestsStatus.expired:
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
