import json
import os
import random

from sqlalchemy.orm import Session
from web3.logs import DISCARD

from . import CONTRACT_ADDRESS, OWNER_ADDRESS, APP_PATH, crud, schemas
from .monsters import COMMON_MONSTERS
from .utils import transform_raw_monster_to_db_monster, transform_db_monster_to_monster_view
from .web3utils import web3

address = CONTRACT_ADDRESS
with open(os.path.join(APP_PATH, "..", "build", "contracts", "GameItems.json"), "r") as f:
    contractData = json.load(f)
    abi = contractData["abi"]
    _contract = web3.eth.contract(address=address, abi=abi)


def create_monster(db: Session, receiver: str):
    random_monster = random.choice(COMMON_MONSTERS)

    # Blockchain stuffs
    nonce = web3.eth.getTransactionCount(OWNER_ADDRESS)
    tx = _contract.functions.createMonster(
        receiver,
        random_monster["name"]
    ).buildTransaction({'nonce': nonce, "from": OWNER_ADDRESS})
    signed_tx = web3.eth.account.signTransaction(tx, os.getenv("PRIVATE_KEY"))
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    event = _contract.events.MonsterCreated().processReceipt(tx_receipt, errors=DISCARD)

    random_monster["id"] = int(event[0]["args"]["MonsterId"])
    monster = transform_raw_monster_to_db_monster(random_monster)
    db_monster = crud.create_db_monster(db, monster)
    return db_monster


def get_user_monsters(db: Session, user: schemas.UserAccount):
    monster_ids = _contract.functions.getUserMonsters(user.address).call()
    monsters = list(map(lambda _id: transform_db_monster_to_monster_view(crud.get_db_monster(db, _id)), monster_ids))
    return schemas.UserMonster(**user.dict(exclude={"key"}), monsters=monsters)
