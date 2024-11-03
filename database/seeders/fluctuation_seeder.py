from app.utils import print_green_bold, model_mapper, json_camel_to_snake, text_to_red
from app.models.Company import CompanyMovingAverage, CompanyRepository
from app.services import StockQuoteService

from core import mongodb
import numpy as np
from datetime import datetime, timedelta


def main():
    """
    This seeder works base on existing symbols in companies collection
    """
    print_green_bold("=== SEEDING FLUCTUATIONS")
    symbols_list = mongodb.query_with_projection(
        CompanyRepository.Meta.collection_name, {}, {"_id": 0, "symbol": 1}
    )
    symbols_list = [record["symbol"] for record in symbols_list]
    quoteService = StockQuoteService()

    # 52w, 200d, 150d, 24d
    for symbol in symbols_list:

        # Get the current date
        current_date = datetime.now().date()
        # Format the current date as YYYY-MM-DD
        today = current_date.strftime("%Y-%m-%d")
        # Calculate the date 52 weeks before today
        date_52_weeks_ago = current_date - timedelta(weeks=52)
        # Format the date 52 weeks ago as YYYY-MM-DD
        today_52w_before = date_52_weeks_ago.strftime("%Y-%m-%d")

        weekly_df = quoteService.history(
            start=today_52w_before, end=today, symbol=symbol, interval="1W"
        ).dropna()

        # calculate 52w average
        avg_52w = weekly_df["close"].tail(52).mean()

        daily_df = quoteService.history(
            start=today_52w_before, end=today, symbol=symbol, interval="1D"
        ).dropna()

        # calculate 200d, 150d, 24d average
        avg_200d = daily_df["close"].tail(200).mean()
        avg_150d = daily_df["close"].tail(150).mean()
        avg_24d = daily_df["close"].tail(24).mean()

        # map the structure
        fluctuation = CompanyMovingAverage(
            week_52=round(avg_52w * 1000, 2),
            day_200=round(avg_200d * 1000, 2),
            day_150=round(avg_150d * 1000, 2),
            day_24=round(avg_24d * 1000, 2),
        ).model_dump()
        # update db
        # mongodb.update_one(
        #     "companies", {"symbol": symbol}, {"fluctuation": fluctuation}
        # )
        mongodb.update_one("stash", {"symbol": symbol}, {"fluctuation": fluctuation})
        print(f"Fluctuation updated for {text_to_red(symbol)}")
    print_green_bold(f"Update fluctuation for {len(symbols_list)} companies")


if __name__ == "__main__" or __name__ == "tasks":
    main()
