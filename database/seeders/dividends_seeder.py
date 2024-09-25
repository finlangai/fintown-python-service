from app.utils import print_green_bold, text_to_red
from app.models import Dividend, DividendRepository
from config.seeder import STOCK_SYMBOLS
from app.services import fireant as fa
import inflection
import pandas as pd


def main():
    print_green_bold("=== SEEDING DIVIDENDS")
    dividendRepo = DividendRepository()
    for symbol in STOCK_SYMBOLS:
        print(f"seeding for {text_to_red(symbol)}")
        result = fa.get_dividends(symbol)
        df = pd.json_normalize(result)

        # select only dividend events
        df = df[df["type"].isin([1, 2])]
        # have the eventID as _id for each document
        df.rename(columns={"eventID": "id"}, inplace=True)
        # rename all columns to snake case
        df.columns = [inflection.underscore(col) for col in df.columns]

        dividends: list[Dividend] = []
        for _, row in df.iterrows():
            dict = row.to_dict()
            dict.update(Dividend.parse_title(dict["title"]))

            dividends.append(Dividend(**dict))
        dividendRepo.save_many(dividends)
        print(f"{len(dividends)} events inserted for {text_to_red(symbol)}")


if __name__ == "__main__" or __name__ == "tasks":
    main()
