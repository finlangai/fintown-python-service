from config.rongviet import *
import urllib.parse, time, json
from app.utils import fetch_url


def get_stock_data(symbol: str):

    # declare the unix time milisecond
    unix = int(time.time() * 1000)
    url = STOCK_DATA_URL.format(unix, symbol)

    return fetch_url(url=url)
