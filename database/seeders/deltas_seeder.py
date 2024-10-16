from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.models.Company import CompanyRepository
from app.services import StockQuoteService

from core import mongodb
import numpy as np, pandas as pd, json
from datetime import datetime, timedelta


def main():
    """
    This seeder works base on existing symbols in companies collection
    """
    print_green_bold("=== SEEDING DELTAS")
    symbols = mongodb.query_with_projection(
        CompanyRepository.Meta.collection_name, {}, {"_id": 0, "symbol": 1}
    )
    symbol_list = [record["symbol"] for record in symbols]

    quoteService = StockQuoteService()

    # Get the current date
    current_date = datetime.now().date()
    # Format the current date as YYYY-MM-DD
    today = current_date.strftime("%Y-%m-%d")
    # Calculate the date 52 weeks before today
    date_52_weeks_ago = current_date - timedelta(weeks=52)
    # Format the date 52 weeks ago as YYYY-MM-DD
    today_52w_before = date_52_weeks_ago.strftime("%Y-%m-%d")

    # delta in day, delta in week, delta in month, delta in year

    for symbol in symbol_list:
        quotes_df = quoteService.history(
            symbol=symbol, start=today_52w_before, end=today, interval="1D"
        )
        quotes_df.set_index("time", inplace=True)
        delta_df = pd.DataFrame()
        close_series = quotes_df["close"] * 1000

        # Calculate Deltas
        delta_df["daily_delta"] = close_series.diff()
        delta_df["weekly_delta"] = close_series.diff(5)  # 5 trading days in a week
        delta_df["monthly_delta"] = close_series.diff(
            21
        )  # Approx 21 trading days in a month

        # Calculate Delta Percentages
        delta_df["daily_delta_pct"] = (
            delta_df["daily_delta"] / close_series.shift(1) * 100
        )
        delta_df["weekly_delta_pct"] = (
            delta_df["weekly_delta"] / close_series.shift(5) * 100
        )
        delta_df["monthly_delta_pct"] = (
            delta_df["monthly_delta"] / close_series.shift(21) * 100
        )

        # Calculate Yearly Delta based on first and last available quotes
        oldest_quote = int(close_series.iloc[0])
        latest_quote = int(close_series.iloc[-1])
        yearly_delta = latest_quote - oldest_quote
        yearly_delta_pct = ((latest_quote - oldest_quote) / oldest_quote) * 100

        # Get the latest deltas and percentages
        latest_row = delta_df.iloc[-1]

        delta_dict = {
            "daily": {
                "change": latest_row["daily_delta"],
                "percent": latest_row["daily_delta_pct"],
            },
            "weekly": {
                "change": latest_row["weekly_delta"],
                "percent": latest_row["weekly_delta_pct"],
            },
            "monthly": {
                "change": latest_row["monthly_delta"],
                "percent": latest_row["monthly_delta_pct"],
            },
            "yearly": {
                "change": yearly_delta,
                "percent": yearly_delta_pct,
            },
        }

        mongodb.update_one("stash", {"symbol": symbol}, {"delta": delta_dict})


if __name__ == "__main__" or __name__ == "tasks":
    main()
