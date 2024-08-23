from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.models import Dividend
from app.services import get_dividends
from core.mongodb import insert_many
from database.seeding_stocks import STOCK_SYMBOLS


def main():
    print_green_bold("=== SEEDING DIVIDENDS")
    for symbol in STOCK_SYMBOLS:
        dividends = [
            model_mapper(Dividend, json_camel_to_snake(raw_obj), {"symbol": symbol})
            for raw_obj in get_dividends(symbol=symbol, count=1000)
        ]

        insert_many(collection_name="dividends", documents=dividends)
        print(f"{text_to_red(symbol.upper())} dividends inserted")


if __name__ == "__main__" or "tasks":
    main()
