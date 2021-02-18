from fastapi import APIRouter

from app.routes.users import user_route
from app.routes.requests import requests_route

router = APIRouter()
router.include_router(user_route, tags=["users"])
router.include_router(requests_route, tags=["requests"])
