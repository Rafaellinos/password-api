from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .users import get_current_active_user
from db.database import get_db
from models.users import UserModel
from models.requests import PasswordRequestsIn, PasswordRequestsOut
from services.requests import (
    create_password,
    get_requests,
    get_request,
    request_password,
    NotFound,
)


requests_route = APIRouter()


@requests_route.get("/request_password")
async def request_key(
        views_limit: int,
        expire_in_days: int,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_active_user),
):

    password_request = PasswordRequestsIn(
        user_id=current_user.id,
        view_counter=views_limit,
        due_date=datetime.now() + timedelta(days=expire_in_days),
    )

    return create_password(current_user.id, db, password_request)


@requests_route.get("/requests", response_model=List[PasswordRequestsOut])
async def get_requests_(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_active_user),
):
    return get_requests(user=current_user.id, db=db)


@requests_route.get("/request/{public_id}", response_model=PasswordRequestsOut)
async def get_request_(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_active_user),
        public_id: str = None,
):
    try:
        return get_request(current_user.id, db, public_id)
    except NotFound:
        raise HTTPException(status_code=404, detail="Request not found")


@requests_route.get("/password/{public_id}")
async def request_password_(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_active_user),
        public_id: str = None,
):
    try:
        return request_password(current_user.id, db, public_id)
    except NotFound:
        raise HTTPException(status_code=404, detail="Password not found.")
