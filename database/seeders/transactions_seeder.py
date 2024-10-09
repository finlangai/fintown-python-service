from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.services import cafef
from app.models import Transaction, TransactionRepository
from app.utils import convert_to_unix_timestamp

from config import STOCK_SYMBOLS
import pandas as pd, numpy as np, inflection, sys


def main():
    print_green_bold("=== SEEDING INTERNAL TRANSACTIONS")

    raw_transactions_data: list[dict] = []
    for symbol in STOCK_SYMBOLS:
        print(f"- fetching transactions data for {text_to_red(symbol)}")
        raw_transactions: list[dict] = cafef.get_internal_transaction(symbol)

        raw_transactions_data.extend(raw_transactions)

    transactions_df = pd.DataFrame(raw_transactions_data)
    transactions_df.columns = [
        inflection.underscore(col) for col in transactions_df.columns
    ]
    transactions_df.rename(
        columns={"stock": "symbol", "ty_le_so_huu": "ownership"}, inplace=True
    )
    date_columns = [
        "plan_begin_date",
        "plan_end_date",
        "real_end_date",
        "published_date",
        "order_date",
    ]

    # take out the unix timestamp of date columns
    for col_name in date_columns:
        transactions_df[col_name] = transactions_df[col_name].apply(
            convert_to_unix_timestamp
        )

    # turn empty string into None
    transactions_df.replace(r"^\s*$", None, regex=True, inplace=True)
    # Turn NaN to None
    transactions_df.replace({np.nan: None}, inplace=True)

    transactions_accumulator: list[Transaction] = []
    for _, row in transactions_df.iterrows():
        transaction_dict = row.to_dict()
        transactions_accumulator.append(Transaction(**transaction_dict))

    TransactionRepository().save_many(models=transactions_accumulator)
    print_green_bold(
        f"{len(transactions_accumulator)} transaction inserted for {len(STOCK_SYMBOLS)} symbols"
    )


if __name__ == "__main__" or __name__ == "tasks":
    main()
