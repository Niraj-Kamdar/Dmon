from pydantic import BaseModel
from pydantic import Field


class UserBase(BaseModel):
    username: str = Field(..., example="john37")


class UserCreate(UserBase):
    password: str = Field(..., example="secret^123$")


class UserAccount(UserBase):
    key: str
    disabled: bool


class User(UserBase):
    id: int
    disabled: bool = Field(..., example=False)

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    message: str
