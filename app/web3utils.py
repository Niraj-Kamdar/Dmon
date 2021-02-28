import secrets

from eth_account import Account
from web3 import Web3, HTTPProvider

from . import RPC_URL
from .utils import secret, Wallet

web3 = Web3(HTTPProvider(RPC_URL))


def create_account(password: str) -> Wallet:
    account = Account.create(secrets.token_urlsafe(16))
    return Wallet(account.address, secret.dumps(account.encrypt(password)))
