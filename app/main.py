import os
import re
from datetime import timedelta

import aiofiles
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import ACCESS_TOKEN_EXPIRE_MINUTES
from . import APP_PATH
from . import crud
from . import models
from . import schemas
from .database import engine
from .utils import create_access_token
from .utils import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
validate_email = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


@app.get("/", response_class=HTMLResponse)
async def index():
    """ Index page of the website """
    index_path = os.path.join(APP_PATH, "static", "index.html")
    async with aiofiles.open(index_path, "r") as f:
        html = await f.read()
    return HTMLResponse(content=html, status_code=200)


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"], "key": user["key"]},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post(
    "/users/",
    response_model=schemas.User,
    responses={
        400: {
            "description": "Invalid request body!",
            "model": schemas.Message
        },
    },
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates new user with the following information:
    - **username** - username of the user that will be used for login
    - **password**: password of the user
    """
    db_user = crud.get_db_user(db, username=user.username)
    if db_user:
        return JSONResponse(
            status_code=400,
            content={
                "message": f"Username: {user.username} already registered"
            },
        )
    db_user = crud.create_db_user(db=db, user=user)
    return db_user


@app.get("/users/me/", response_model=schemas.UserBase)
async def read_users_me(current_user: schemas.UserAccount = Depends(
        crud.get_current_active_user), ):
    """
    Returns information of current user:
    - **username** - username of the user that will be used for login
    """
    return current_user
