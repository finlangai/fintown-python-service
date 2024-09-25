from config.fireant_endpoints import (
    ENDPOINT_DIVIDENDS,
    ENDPOINT_FINANCIAL_STATEMENT,
    ENDPOINT_FUNDAMENTAL,
    ENDPOINT_HOLDERS,
    ENDPOINT_PROFILE,
)
from app.utils import fetch_url


# === GET DIVIDENDS
# def get_dividends(symbol: str, count: int):
#     url = ENDPOINT_DIVIDENDS.format(symbol)
#     params = {"count": count}
#     return fetch_url(url=url, params=params)


def get_dividends(
    symbol: str,
    limit: int = 1000,
    type: int = 0,
    offset: int = 0,
    order_by: int = 1,
    start_date="2000-01-01",
    end_date="2034-09-25",
):
    url = ENDPOINT_DIVIDENDS
    params = {
        "symbol": symbol,
        "limit": limit,
        "type": type,
        "offset": offset,
        "orderBy": order_by,
        "startDate": start_date,
        "endDate": end_date,
    }
    return fetch_url(url=url, params=params)


# === GET FINANCIAL STATEMENT
from datetime import datetime
from app.enums import StatementType


def get_financial_statement(
    symbol: str,
    type: StatementType,
    limit: int,
    quarter: int = 4,
    year: int = datetime.now().year,
):

    url = ENDPOINT_FINANCIAL_STATEMENT.format(symbol)
    params = {
        "type": type.value,
        "year": year,
        "quarter": quarter,
        "limit": limit,
    }

    return fetch_url(url=url, params=params)


# === GET HOLDERS
def get_holders(symbol: str):
    url = ENDPOINT_HOLDERS.format(symbol)
    return fetch_url(url)


# === GET HOLDERS
def get_profile(symbol: str):
    url = ENDPOINT_PROFILE.format(symbol)
    return fetch_url(url)


# === GET HOLDERS
def get_fundamental(symbol: str):
    url = ENDPOINT_FUNDAMENTAL.format(symbol)
    return fetch_url(url)
