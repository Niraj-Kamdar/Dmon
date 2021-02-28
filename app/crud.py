from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from . import ALGORITHM, models, schemas, SECRET_KEY
from .utils import get_db, get_key
from .web3utils import create_account

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(db: Session = Depends(get_db),
                           token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        key: str = payload.get("key")
        if username is None or key is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_user = get_db_user(db, username=username)
    if db_user is None:
        raise credentials_exception
    user = schemas.UserAccount(key=key, **db_user.dict())
    return user


async def get_current_active_user(
        current_user: schemas.UserAccount = Depends(get_current_user), ):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_db_user(db: Session, username: str):
    return db.query(
            models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_db_user(db, username)
    if not user:
        return False
    key = get_key(password, user.hashed_key)
    if not key:
        return False
    return {"username": user.username, "key": key}


def create_db_user(db: Session, user: schemas.UserCreate):
    dict_user = user.dict(exclude={"password"})
    new_wallet = create_account(user.password)
    dict_user["hashed_key"] = new_wallet.key
    dict_user["address"] = new_wallet.address
    db_user = models.User(**dict_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_db_monster(db: Session, monster: schemas.MonsterCreate):
    db_monster = models.Monster(**monster.dict())
    db.add(db_monster)
    db.commit()
    db.refresh(db_monster)
    return db_monster


def get_db_monster(db: Session, monster_id: int):
    return db.query(
            models.Monster).filter(models.Monster.id == monster_id).first()
