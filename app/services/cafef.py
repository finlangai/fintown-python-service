from config.cafef import ENDPOINT_INTERNAL_TRANSACTION, ENDPOINT_PRICE_HISTORY
from app.utils import fetch_url


def get_internal_transaction(symbol: str):
    url = ENDPOINT_INTERNAL_TRANSACTION.format(symbol)
    return fetch_url(url)["Data"]["Data"]


def get_price_history(symbol: str):
    url = ENDPOINT_PRICE_HISTORY.format(symbol)
    return fetch_url(url)["Data"]["Data"]
