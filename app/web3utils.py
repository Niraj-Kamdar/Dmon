import secrets

from web3 import Web3, HTTPProvider
from eth_account import Account

from app.utils import secret


def get_web3():
    web3 = Web3(HTTPProvider("https://rpc-mumbai.maticvigil.com/v1/6024ee92e578292ef2a1f5ac576166e4d43b7d73"))
    try:
        yield web3
    finally:
        del web3


def create_account(password: str) -> str:
    account = Account.create(secrets.token_urlsafe(16))
    return secret.dumps(account.encrypt(password))
