from app.utils import (
    print_green_bold,
    model_mapper,
    json_camel_to_snake,
    text_to_red,
    time,
)
from app.services import (
    StockFinanceService,
    FormularResolver,
    StockQuoteService,
)
from app.enums import ParamLocation
from core import mongodb
from datetime import timedelta, datetime
import numpy as np, pandas as pd

from database.seeders import stash_stats_seeder


def main():
    """
    This seeder update stats for vn30
    """
    print_green_bold("=== UPDATING VN30 STASH")
    financeService = FormularResolver(period="quarter")

    vn30_list = financeService.stock.listing.symbols_by_group("VN30")
    sum_marketcap = 0
    sum_earnings = 0
    sum_equity = 0
    sum_revenue = 0

    for symbol in vn30_list:
        financeService.update_symbol(symbol=symbol)

        # get required df
        ratio_df = financeService.get_data(ParamLocation.ratio)
        income_df = financeService.get_data(ParamLocation.income_statement)
        balance_df = financeService.get_data(ParamLocation.balance_sheet)

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

    daily_df = quoteService.history(
        symbol="VN30",
        interval="1D",
        start=time.date_from(timedelta(days=5)),
        end=today,
    ).iloc[::-1]

    VN30_LAST_CLOSED = float(daily_df.iloc[0]["close"])
    vn30_day_before_yesterday_closed = float(daily_df.iloc[1]["close"])
    VN30_DELTA_VALUE = VN30_LAST_CLOSED - vn30_day_before_yesterday_closed
    VN30_DELTA_PERCENT = VN30_DELTA_VALUE / vn30_day_before_yesterday_closed * 100

    # === CALCUALTE 52W MEAN
    date_52_weeks_ago = current_date - timedelta(weeks=52)
    # Format the date 52 weeks ago as YYYY-MM-DD
    today_52w_before = date_52_weeks_ago.strftime("%Y-%m-%d")

    weekly_df = quoteService.history(
        start=today_52w_before, end=today, symbol="VN30", interval="1W"
    ).dropna()
    AVG_52W = weekly_df["close"].tail(52).mean()

    VN30_PE = sum_marketcap / sum_earnings
    VN30_PB = sum_marketcap / sum_equity

    vn30_stash = {
        "symbol": "VN30",
        "is_stock": False,
        "pe": round(float(VN30_PE), 2),
        "pb": round(float(VN30_PB), 2),
        "avg52w": round(float(AVG_52W), 2),
        "marketcap": int(sum_marketcap),
        "earnings": int(sum_earnings),
        "revenue": int(sum_revenue),
        # "equity": int(sum_equity),
        "vn30LastClosed": round(VN30_LAST_CLOSED, 2),
        "vn30DeltaValue": round(VN30_DELTA_VALUE, 2),
        "vn30DeltaPercent": round(VN30_DELTA_PERCENT, 2),
    }
    mongodb.update_one("stash", {"symbol": "VN30"}, vn30_stash)
    print_green_bold(f"VN30 stash updated")


if __name__ == "__main__" or __name__ == "tasks":
    main()
