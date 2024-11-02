from app.utils import (
    print_green_bold,
    text_to_red,
    text_to_blue,
)
from app.models import StockQuote, StockQuoteRepository
from app.services import StockQuoteService
from app.enums import QuoteInterval
from app.types import IntervalType
from config.seeder import STOCK_SYMBOLS, INDEX_SYMBOLS

from datetime import datetime
import numpy as np


def main():
    print_green_bold("=== SEEDING QUOTES")

    quoteService = StockQuoteService()
    stockQuoteRepo = StockQuoteRepository()
    # get the list of interval for getting interval string value
    interval_list = IntervalType.__args__

    for symbol in STOCK_SYMBOLS:
        print(f"=== seeding quotes for {text_to_red(symbol)}")
        stock_quotes: list[StockQuote] = []

        for interval_index in QuoteInterval:

            today = datetime.today().strftime("%Y-%m-%d")
            interval_name = interval_list[interval_index.value]

            quotes_df = quoteService.history(
                symbol=symbol,
                start="2000-01-01",
                end=today,
                interval=interval_name,
            )

            # replace NaN with None
            # quotes_df = quotes_df.replace(np.nan, None)

            # drop row that are NaN
            quotes_df.dropna(inplace=True)

            # convert time column to unix timestamp
            quotes_df["time"] = quotes_df["time"].apply(lambda x: int(x.timestamp()))

            columns_to_multiply = ["open", "high", "low", "close"]
            quotes_df[columns_to_multiply] = quotes_df[columns_to_multiply].apply(
                lambda x: x * 1000
            )

            # add interval column
            quotes_df.insert(loc=0, column="interval", value=interval_index.value)

            # add symbol column
            quotes_df.insert(loc=0, column="symbol", value=symbol)

            # loop through each row in the dataframe and accumulate Quotes model into events variable
            for _, row in quotes_df.iterrows():
                dict = row.to_dict()
                stock_quotes.append(StockQuote(**dict))

            print(f"{text_to_blue(interval_name)} interval has {len(quotes_df)} quotes")

        # insert db
        stockQuoteRepo.save_many(stock_quotes)

        print(f"{len(stock_quotes)} inserted for {text_to_red(symbol)} ===")


if __name__ == "__main__" or __name__ == "tasks":
    main()
