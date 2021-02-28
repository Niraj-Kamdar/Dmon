from typing import List

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., example="john37")


class UserCreate(UserBase):
    password: str = Field(..., example="secret^123$")


class UserAccount(UserBase):
    id: int
    address: str
    key: str
    disabled: bool


class User(UserBase):
    id: int
    address: str = Field(..., example="0x29D9C4405A72ffa26eB13218b7C29F98F2B21aD0")
    disabled: bool = Field(..., example=False)

    class Config:
        orm_mode = True


class MonsterStats(BaseModel):
    power: int
    attackXp: int
    defenseXp: int
    healthXp: int


class MonsterProperty(BaseModel):
    rarity: str
    type: str
    stats: MonsterStats


class MonsterBase(BaseModel):
    id: int
    name: str
    description: str
    image: str


class MonsterCreate(MonsterBase):
    rarity: str
    type: str
    power: int
    attack_xp: int
    defense_xp: int
    health_xp: int


class Monster(MonsterCreate):
    id: int

    class Config:
        orm_mode = True


class MonsterView(MonsterBase):
    properties: MonsterProperty


class UserMonster(UserBase):
    id: int
    address: str = Field(..., example="0x29D9C4405A72ffa26eB13218b7C29F98F2B21aD0")
    disabled: bool = Field(..., example=False)
    monsters: List[MonsterView]


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    message: str
