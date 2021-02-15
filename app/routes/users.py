from fastapi import Depends, HTTPException, status, APIRouter
from jose import JWTError, jwt
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config.settings import get_settings
from models.users import User, Token, UserModel, UserIn
from db.database import get_db
from services.users import (
    get_user,
    authenticate_user,
    create_access_token,
    create_user,
)


user_route = APIRouter()
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login")


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@user_route.post("/login", response_model=Token)
async def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(seconds=settings.REGISTRATION_TOKEN_LIFETIME)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_route.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: UserModel = Depends(get_current_active_user),
):
    return {"username": current_user.username, "is_active": current_user.is_active}


@user_route.post("/users/", response_model=User)
def create_user_(
    user: UserIn, db: Session = Depends(get_db),
):

    return create_user(db=db, user=user)
