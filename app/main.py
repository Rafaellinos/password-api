from fastapi import FastAPI
import uvicorn

from routes.routes import router
from config.settings import get_settings


settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

app.include_router(
    router,
    prefix=settings.API_PREFIX,
)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
    )

# from typing import List, Optional
# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
# from fastapi import Depends, FastAPI, HTTPException, status
# from jose import JWTError, jwt
# import logging
#
# from . import crud, models, schemas
# from .database import SessionLocal, engine
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#
# models.Base.metadata.create_all(bind=engine)
#
# app = FastAPI(
#     title="Pass Generator",
#     debug=True,
# )
#
# logger = logging.getLogger("uvicorn.error")
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     except:
#         db.rollback()
#     finally:
#         db.close()
#
#
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# # async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Could not validate credentials",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     try:
# #         payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
# #         username: str = payload.get("sub")
# #         if username is None:
# #             raise credentials_exception
# #         token_data = username
# #     except JWTError:
# #         raise credentials_exception
# #     user = crud.get_user(db, username=token_data)
# #     if user is None:
# #         raise credentials_exception
# #     return user
# #
# #
# # async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
# #     if not current_user.is_active:
# #         raise HTTPException(status_code=400, detail="Inactive user")
# #     return current_user
# #
# #
# # @app.post("/login", response_model=schemas.Token)
# # async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
# #     user = crud.authenticate_user(db, form_data.username, form_data.password)
# #     if not user:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Incorrect username or password",
# #             headers={"WWW-Authenticate": "Bearer"},
# #         )
# #     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# #
# #     access_token = crud.create_access_token(
# #         data={"sub": user.username}, expires_delta=access_token_expires
# #     )
# #     return {"access_token": access_token, "token_type": "bearer"}
# #
# #
# # @app.get("/users/me/", response_model=schemas.User)
# # async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
# #     return {"username": current_user.username, "is_active": current_user.is_active}
# #
# #
# # @app.post("/users/", response_model=schemas.User)
# # def create_user(
# #     user: schemas.UserIn, db: Session = Depends(get_db),
# # ):
# #     return crud.create_user(db=db, user=user)
#
#
# @app.get("/request_password")
# async def request_key(
#         views_limit: int,
#         expire_in_days: int,
#         db: Session = Depends(get_db),
#         current_user: models.User = Depends(get_current_active_user),
# ):
#
#     password_request = schemas.PasswordRequestsIn(
#         user_id=current_user.id,
#         view_counter=views_limit,
#         due_date=datetime.now() + timedelta(days=expire_in_days),
#     )
#
#     teste = crud.create_password(current_user.id, db, password_request)
#     return teste
#
#
# @app.get("/requests", response_model=List[schemas.PasswordRequestsOut])
# async def get_requests(
#         db: Session = Depends(get_db),
#         current_user: models.User = Depends(get_current_active_user),
# ):
#     return crud.get_requests(user=current_user.id, db=db)
#
#
# @app.get("/request/{public_id}", response_model=schemas.PasswordRequestsOut)
# async def get_request(
#         db: Session = Depends(get_db),
#         current_user: models.User = Depends(get_current_active_user),
#         public_id: str = None,
# ):
#     return crud.get_request(current_user.id, db, public_id)
#
#
# @app.get("/password/{public_id}")
# async def request_password(
#         db: Session = Depends(get_db),
#         current_user: models.User = Depends(get_current_active_user),
#         public_id: str = None,
# ):
#     return crud.request_password(current_user.id, db, public_id)
