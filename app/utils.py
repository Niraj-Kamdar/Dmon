from datetime import datetime
from datetime import timedelta
from typing import Optional

from eth_account import Account
from itsdangerous import JSONWebSignatureSerializer
from jose import jwt
from web3 import Web3

from . import ALGORITHM
from . import SECRET_KEY
from .database import SessionLocal


class Secret:
    def __init__(self):
        self.secret = JSONWebSignatureSerializer(SECRET_KEY)

    def dumps(self, obj):
        dumped = self.secret.dumps(obj)
        return dumped.decode('utf-8')

    def loads(self, s):
        return self.secret.loads(s.encode('utf-8'))


secret = Secret()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_key(password, hashed_key):
    encrypted = secret.loads(hashed_key)
    return Web3.toHex(Account.decrypt(encrypted, password))
