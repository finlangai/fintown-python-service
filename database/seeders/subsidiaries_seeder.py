from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.services import StockInfoService
from app.models import Subsidiary, SubsidiaryRepository
from config.seeder import STOCK_SYMBOLS


def main():
    print_green_bold("=== SEEDING SUBSIDIARIES")

    infoService = StockInfoService()
    subsidiaryRepo = SubsidiaryRepository()

    for symbol in STOCK_SYMBOLS:
        # update symbol
        infoService.update_symbol(symbol)

        # get events dataframe of the company
        subsidiaries_df = infoService.subsidiaries()

        # add symbol column
        subsidiaries_df.insert(0, "symbol", symbol)

        # loop through each row in the dataframe and accumulate News model into events variable
        subsidiaries: list[Subsidiary] = []
        for _, row in subsidiaries_df.iterrows():
            dict = row.to_dict()
            subsidiaries.append(Subsidiary(**dict))

        # insert db
        subsidiaryRepo.save_many(subsidiaries)

        print(f"{len(subsidiaries)} subsidiaries inserted for {text_to_red(symbol)}")


if __name__ == "__main__" or __name__ == "tasks":
    main()
