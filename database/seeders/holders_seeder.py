from app.models import Holder
from database.seeders import STOCK_SYMBOLS
from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red

from core.mongodb import insert_many
from app.services.fireant import get_holders


def main():
    print_green_bold("=== SEEDING HOLDERS")
    for symbol in STOCK_SYMBOLS:
        holders = [
            model_mapper(Holder, json_camel_to_snake(raw_obj), {"symbol": symbol})
            for raw_obj in get_holders(symbol)
        ]

        insert_many(collection_name="holders", documents=holders)
        print(f"{text_to_red(symbol.upper())} holders inserted")


if __name__ == "__main__" or __name__ == "tasks":
    main()
