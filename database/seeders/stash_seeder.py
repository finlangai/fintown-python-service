from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.services import (
    StockFinanceService,
    FormularResolver,
    StockQuoteService,
    StockInfoService,
)
from app.enums import ParamLocation
from config.seeder import STOCK_SYMBOLS
from core import mongodb
from datetime import timedelta, datetime
import numpy as np, pandas as pd

from database.seeders import stash_stats_seeder


def main():
    """
    This seeder only seed symbol, last 5 quarterly and yearly record of revenue, equity, net_profit
    And VN30 summary
    """
    print_green_bold("=== SEEDING STASH")
    financeService = FormularResolver(period="quarter")
    infoService = StockInfoService()

    stash_holder: list = []

    vn30_list = financeService.stock.listing.symbols_by_group("VN30")
    sum_marketcap = 0
    sum_earnings = 0
    sum_equity = 0
    sum_revenue = 0

    period_list = ["quarter", "year"]
    for symbol in vn30_list:
        financeService.update_symbol(symbol=symbol)
        infoService.update_symbol(symbol=symbol)

        company_info = infoService.overview()
        company_stash = {
            "symbol": symbol,
            "industry": company_info["industry"],
            "exchange": company_info["exchange"],
            "quarter": [],
            "year": [],
        }

        for period in period_list:
            financeService.update_period(period)

            # get required df
            ratio_df = financeService.get_data(ParamLocation.ratio)
            income_df = financeService.get_data(ParamLocation.income_statement)
            balance_df = financeService.get_data(ParamLocation.balance_sheet)

            stash_df = financeService.get_meta_df().head()

            income_stash = income_df.head()[
                [
                    "Net Profit For the Year",
                    "Revenue (Bn. VND)",
                ]
            ]
            balance_stash = balance_df.head()[["OWNER'S EQUITY(Bn.VND)"]]

            # merge dataframes
            stash_df = pd.concat([stash_df, income_stash, balance_stash], axis=1)
            rename_dict = {
                "yearReport": "year",
                "Net Profit For the Year": "net_profit",
                "Revenue (Bn. VND)": "revenue",
                "OWNER'S EQUITY(Bn.VND)": "equity",
            }
            # rename the quarter column if is quarter period
            if period == "quarter":
                rename_dict.update({"lengthReport": "quarter"})

            # rename column for inserting
            stash_df.rename(
                columns=rename_dict,
                inplace=True,
            )

            for _, row in stash_df.iterrows():
                company_stash[period].append(row.to_dict())

        # append the stash to holder for later insert
        stash_holder.append(company_stash)
        print_green_bold(f"generate stashed for {symbol}")

        # sum for vn30
        sum_marketcap += ratio_df.iloc[0]["Market Capital (Bn. VND)"]
        sum_earnings += income_df.iloc[0]["Net Profit For the Year"]
        sum_revenue += income_df.iloc[0]["Revenue (Bn. VND)"]
        sum_equity += balance_df.iloc[0]["OWNER'S EQUITY(Bn.VND)"]

    # ======================================================
    # ==================CALCULATE FOR V30===================
    # ======================================================
    # calculate 52w mean
    quoteService = StockQuoteService()

    # Get the current date
    current_date = datetime.now().date()
    # Format the current date as YYYY-MM-DD
    today = current_date.strftime("%Y-%m-%d")
    # Calculate the date 52 weeks before today
    date_52_weeks_ago = current_date - timedelta(weeks=52)
    # Format the date 52 weeks ago as YYYY-MM-DD
    today_52w_before = date_52_weeks_ago.strftime("%Y-%m-%d")

    weekly_df = quoteService.history(
        start=today_52w_before, end=today, symbol="VN30", interval="1W"
    ).dropna()
    avg_52w = weekly_df["close"].tail(52).mean()

    pevn30 = sum_marketcap / sum_earnings
    pbvn30 = sum_marketcap / sum_equity

    vn30_stash = {
        "symbol": "VN30",
        "pe": float(pevn30),
        "pb": float(pbvn30),
        "avg_52w": float(avg_52w),
        "marketcap": int(sum_marketcap),
        "earnings": int(sum_earnings),
        "revenue": int(sum_revenue),
        "equity": int(sum_equity),
    }
    stash_holder.append(vn30_stash)
    mongodb.insert_many("stash", stash_holder)
    print_green_bold(f"{len(stash_holder)} stash inserted")

    # ======================================================
    # ====================RELATED SEEDER====================
    # ======================================================
    # related seeder
    from database.seeders import deltas_seeder, best_npm_seeder

    deltas_seeder.main()
    best_npm_seeder.main()
    stash_stats_seeder.main()


if __name__ == "__main__" or __name__ == "tasks":
    main()
