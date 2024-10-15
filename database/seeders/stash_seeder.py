from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.services import StockFinanceService, FormularResolver
from app.enums import ParamLocation
from config.seeder import STOCK_SYMBOLS
from core import mongodb

import numpy as np, pandas as pd


def main():
    print_green_bold("=== SEEDING STASH")
    financeService = FormularResolver(period="quarter")

    stash_holder: list = []

    vn30_list = financeService.stock.listing.symbols_by_group("VN30")
    sum_marketcap = 0
    sum_earnings = 0
    sum_equity = 0
    sum_revenue = 0

    for symbol in vn30_list:
        financeService.update_symbol(symbol=symbol)

        ratio_df = financeService.get_data(ParamLocation.ratio)

        income_df = financeService.get_data(ParamLocation.income_statement)
        balance_df = financeService.get_data(ParamLocation.balance_sheet)

        company_stash = {"symbol": symbol, "historical": []}
        stash_df = financeService.get_meta_df().head()

        income_stash = income_df.head()[
            [
                "Net Profit For the Year",
                "Revenue (Bn. VND)",
            ]
        ]
        balance_stash = balance_df.head()[["OWNER'S EQUITY(Bn.VND)"]]

        stash_df = pd.concat([stash_df, income_stash, balance_stash], axis=1)
        # rename column for inserting
        stash_df.rename(
            columns={
                "yearReport": "year",
                "lengthReport": "quarter",
                "Net Profit For the Year": "net_profit",
                "Revenue (Bn. VND)": "revenue",
                "OWNER'S EQUITY(Bn.VND)": "equity",
            },
            inplace=True,
        )
        for _, row in stash_df.iterrows():
            company_stash["historical"].append(row.to_dict())

        stash_holder.append(company_stash)
        print_green_bold(f"generate stashed for {symbol}")

        # sum for vn30
        sum_marketcap += ratio_df.iloc[0]["Market Capital (Bn. VND)"]
        sum_earnings += income_df.iloc[0]["Net Profit For the Year"]
        sum_revenue += income_df.iloc[0]["Revenue (Bn. VND)"]
        sum_equity += balance_df.iloc[0]["OWNER'S EQUITY(Bn.VND)"]

    pevn30 = sum_marketcap / sum_earnings
    pbvn30 = sum_marketcap / sum_equity

    vn30_stash = {
        "symbol": "VN30",
        "pe": float(pevn30),
        "pb": float(pbvn30),
        "marketcap": int(sum_marketcap),
        "earnings": int(sum_earnings),
        "revenue": int(sum_revenue),
        "equity": int(sum_equity),
    }
    stash_holder.append(vn30_stash)
    mongodb.insert_many("stash", stash_holder)
    print_green_bold(f"{len(stash_holder)} stash inserted")


if __name__ == "__main__" or __name__ == "tasks":
    main()
