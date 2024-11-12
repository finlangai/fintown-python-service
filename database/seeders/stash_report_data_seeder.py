from app.utils import (
    print_green_bold,
    model_mapper,
    json_camel_to_snake,
    text_to_red,
    time,
)
from app.models import CompanyRepository, FormularRepository
from app.services import StockQuoteService, FormularResolver
from app.enums import ParamLocation

from core import mongodb
import numpy as np, pandas as pd, json
from datetime import timedelta


def main():
    """ """
    print_green_bold("=== SEEDING REPORT DATA FOR STASH")
    # get the list of symbol from companies symbol
    symbols = mongodb.query_with_projection(
        CompanyRepository.Meta.collection_name, {}, {"_id": 0, "symbol": 1}
    )
    symbol_list = [record["symbol"] for record in symbols]

    financeService = FormularResolver(period="quarter")

    for symbol in symbol_list:
        financeService.update_symbol(symbol)

        latest_report = {}
        balance_df = financeService.balance_sheet()
        balance_first_row = balance_df.head()[
            ["LIABILITIES (Bn. VND)", "Cash and cash equivalents (Bn. VND)"]
        ].iloc[0]

        latest_report["liabilities"] = int(balance_first_row["LIABILITIES (Bn. VND)"])
        latest_report["cash_and_cash_equivalents"] = int(
            balance_first_row["Cash and cash equivalents (Bn. VND)"]
        )

        mongodb.update_one(
            "stash", {"symbol": symbol}, {"latest_report": latest_report}
        )
        print_green_bold(f"report data updated for {symbol}")


if __name__ == "__main__" or __name__ == "tasks":
    main()
