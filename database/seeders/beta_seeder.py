from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.models.Company import CompanyRepository
from app.services import StockQuoteService, rongviet

from core import mongodb
import numpy as np, pandas as pd, json
from datetime import datetime, timedelta


def main():
    """
    Get the newest beta value for symbol
    """
    print_green_bold("=== SEEDING BETA")
    symbols = mongodb.query_with_projection(
        CompanyRepository.Meta.collection_name, {}, {"_id": 0, "symbol": 1}
    )
    symbol_list = [record["symbol"] for record in symbols]

    for symbol in symbol_list:
        try:
            beta = rongviet.get_stock_data(symbol)[0]["Beta"]
            mongodb.update_one("stash", {"symbol": symbol}, {"beta": beta})
            print(f"Successfully get Beta value for {symbol}")
        except:
            print(f"An error occured when seeding beta value for {symbol}")


if __name__ == "__main__" or __name__ == "tasks":
    main()
