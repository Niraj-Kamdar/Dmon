from datetime import datetime, timedelta
from typing import Optional, NamedTuple

from eth_account import Account
from itsdangerous import JSONWebSignatureSerializer
from jose import jwt
from web3 import Web3

from . import ALGORITHM, models, schemas, SECRET_KEY
from .database import SessionLocal


class Wallet(NamedTuple):
    address: str
    key: str


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


def transform_db_monster_to_monster_view(db_monster: models.Monster):
    monster_stats = schemas.MonsterStats(
            power=db_monster.power,
            attackXp=db_monster.attack_xp,
            defenseXp=db_monster.defense_xp,
            healthXp=db_monster.health_xp
    )
    monster_property = schemas.MonsterProperty(
            rarity=db_monster.rarity,
            type=db_monster.type,
            stats=monster_stats
    )
    monster = schemas.MonsterView(
            id=db_monster.id,
            name=db_monster.name,
            description=db_monster.description,
            image=db_monster.image,
            properties=monster_property
    )
    return monster


def transform_raw_monster_to_db_monster(monster):
    monster = schemas.MonsterCreate(
            id=monster["id"],
            name=monster["name"],
            description=monster["description"],
            image=monster["image"],
            rarity=monster["properties"]["rarity"],
            type=monster["properties"]["type"],
            power=monster["properties"]["base_stats"]["power"],
            attack_xp=monster["properties"]["base_stats"]["attackXP"],
            defense_xp=monster["properties"]["base_stats"]["defenseXP"],
            health_xp=monster["properties"]["base_stats"]["healthXP"],
    )
    return monster
