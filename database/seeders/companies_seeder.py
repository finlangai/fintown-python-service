from app.utils import model_mapper, print_green_bold, json_camel_to_snake, text_to_red
from app.services import fireant as fa
from app.models import Company, CompanyRepository
from config.seeder import STOCK_SYMBOLS
from app.services import StockInfoService
from config.firebase import FIREBASE_LOGO_URL
from core import mongodb

import os


def main():
    try:
        print_green_bold("=== SEEDING COMPANIES")
        info_service = StockInfoService()
        bucket_name = os.getenv("FIREBASE_BUCKET_NAME")
        for symbol in STOCK_SYMBOLS:
            # switch symbol
            info_service.update_symbol(symbol)

            raw: dict = json_camel_to_snake(fa.get_profile(symbol))
            raw.update(json_camel_to_snake(fa.get_fundamental(symbol)))
            raw.update(info_service.overview())
            raw.update(info_service.profile())

            record = model_mapper(
                model=Company, data=raw, shifted_fields={"symbol": symbol}
            )
            record["symbol"] = symbol
            record["logo"] = FIREBASE_LOGO_URL.format(
                bucket_name=bucket_name, image_name=f"{symbol}.jpeg"
            )

            mongodb.insert_one(collection_name="companies", document=record)

            print(f"{text_to_red(symbol.upper())} profile inserted")
    except Exception as e:
        e.with_traceback()
        print(e)


if __name__ == "__main__" or __name__ == "tasks":
    main()
