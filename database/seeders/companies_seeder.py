from app.utils import model_mapper, print_green_bold, json_camel_to_snake, text_to_red
from app.services import fireant as fa
from app.models import Company, CompanyRepository
from config.seeder import STOCK_SYMBOLS
from app.services import StockInfoService
from core import mongodb


def main():
    try:
        print_green_bold("=== SEEDING COMPANIES")
        info_service = StockInfoService()
        for symbol in STOCK_SYMBOLS:
            # switch symbol
            info_service.update_symbol(symbol)

            raw: dict = json_camel_to_snake(fa.get_profile(symbol))
            raw.update(info_service.overview())
            raw.update(info_service.profile())
            record = model_mapper(
                model=Company, data=raw, shifted_fields={"symbol": symbol}
            )

            mongodb.insert_one(collection_name="companies", document=record)

            print(f"{text_to_red(symbol.upper())} profile inserted")
    except Exception as e:
        e.with_traceback()
        print(e)


if __name__ == "__main__" or __name__ == "tasks":
    main()
