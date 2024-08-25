from app.utils import model_mapper, print_green_bold, json_camel_to_snake, text_to_red
from app.services import fireant as fa
from core import mongodb
from app.models import Company

from database.seeding_stocks import STOCK_SYMBOLS


def main():
    try:
        print_green_bold("=== SEEDING COMPANIES")
        for symbol in STOCK_SYMBOLS:
            raw = json_camel_to_snake(fa.get_profile(symbol))
            profile = model_mapper(
                model=Company, data=raw, shifted_fields={"_id": symbol}
            )

            mongodb.insert_one(collection_name="companies", document=profile)

            print(f"{text_to_red(symbol.upper())} profile inserted")
    except Exception as e:
        print(e)


if __name__ == "__main__" or __name__ == "tasks":
    main()
