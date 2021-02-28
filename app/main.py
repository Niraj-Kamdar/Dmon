import os
import re
from datetime import timedelta

import aiofiles
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import ACCESS_TOKEN_EXPIRE_MINUTES, APP_PATH, crud, models, schemas
from . import contract
from .crud import get_db_monster
from .database import engine
from .utils import create_access_token, transform_db_monster_to_monster_view, get_db

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
        response_model=schemas.UserMonster,
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
    db_monster = contract.create_monster(db, db_user.address)
    monster = transform_db_monster_to_monster_view(db_monster)
    return schemas.UserMonster(**db_user.dict(), monsters=[monster])


@app.get("/users/me/", response_model=schemas.UserAccount)
async def read_users_me(current_user: schemas.UserAccount = Depends(
        crud.get_current_active_user)):
    """
    Returns information of current user:
    - **username** - username of the user that will be used for login
    """
    return current_user


@app.get(
        "/item/{item_id}",
        response_model=schemas.MonsterView,
        responses={
            400: {
                "description": "Invalid request body!",
                "model": schemas.Message
            },
        },
)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    if item_id > 0:
        db_monster = get_db_monster(db, item_id)
        return transform_db_monster_to_monster_view(db_monster)
    return JSONResponse(
        status_code=400,
        content={"message": f"item_id: {item_id} is invalid!"},
    )


@app.get(
    "/monsters",
    response_model=schemas.UserMonster,
    responses={
        400: {
            "description": "Invalid request body!",
            "model": schemas.Message
        },
    },
)
async def get_user_monsters(
    db: Session = Depends(get_db),
    current_user: schemas.UserAccount = Depends(crud.get_current_active_user)
):
    return contract.get_user_monsters(db, current_user)
