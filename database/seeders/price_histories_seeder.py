from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.services import cafef
from app.models import Transaction, TransactionRepository
from app.utils import convert_to_unix_timestamp

from config import STOCK_SYMBOLS
import pandas as pd, numpy as np, inflection, sys


def main():
    """
    PROHIBITED
    """
    print_green_bold("=== SEEDING PRICE HISTORIES")

    raw_price_histories: list[dict] = []
    for symbol in ["VCB"]:
        print(f"- fetching price histories data for {text_to_red(symbol)}")
        raw_history: list[dict] = cafef.get_price_history(symbol)
        raw_price_histories.extend(raw_history)

    price_histories_df = pd.DataFrame(raw_price_histories)
    # price_histories_df.columns = [
    #     inflection.underscore(col) for col in price_histories_df.columns
    # ]

    rename_dict = {
        "GiaCaoNhat": "high",
        "GiaDieuChinh": "adjusted_close",
        "GiaDongCua": "close",
        "GiaMoCua": "open",
        "GiaTriKhopLenh": "value",
        "GiaThapNhat": "low",
        "KhoiLuongKhopLenh": "volume",
        "Ngay": "date",
        "ThayDoi": "delta",
    }
    # price_histories_df.rename(
    #     columns={"stock": "symbol", "ty_le_so_huu": "ownership"}, inplace=True
    # )

    # turn empty string into None
    price_histories_df.replace(r"^\s*$", None, regex=True, inplace=True)

    # Turn NaN to None
    price_histories_df.replace({np.nan: None}, inplace=True)
    print(price_histories_df)

    histories_accumulator: list[Transaction] = []
    # for _, row in price_histories_df.iterrows():
    #     history_dict = row.to_dict()
    #     histories_accumulator.append(Transaction(**history_dict))

    # TransactionRepository().save_many(models=histories_accumulator)
    print_green_bold(
        f"{len(histories_accumulator)} transaction inserted for {len(["VCB"])} symbols"
    )


if __name__ == "__main__" or __name__ == "tasks":
    main()
