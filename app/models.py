from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_key = Column(String)
    address = Column(String, unique=True, index=True)
    disabled = Column(Boolean, default=False)


class Monster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    image = Column(String)
    rarity = Column(String)
    type = Column(String)
    power = Column(Integer)
    attack_xp = Column(Integer)
    defense_xp = Column(Integer)
    health_xp = Column(Integer)
