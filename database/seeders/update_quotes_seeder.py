from app.utils import (
    print_green_bold,
    text_to_red,
    text_to_blue,
)
from app.models import StockQuote, StockQuoteRepository, CompanyRepository
from app.services import StockQuoteService
from app.enums import QuoteInterval
from app.types import IntervalType
from config.seeder import STOCK_SYMBOLS, INDEX_SYMBOLS
from core import mongodb

from datetime import datetime
import numpy as np


def main():
    print_green_bold("=== GETTING LATEST QUOTES")

    quoteService = StockQuoteService()
    stockQuoteRepo = StockQuoteRepository()
    # get the list of interval for getting interval string value
    interval_list = IntervalType.__args__

    symbols = mongodb.query_with_projection(
        CompanyRepository.Meta.collection_name, {}, {"_id": 0, "symbol": 1}
    )
    symbols_list = [record["symbol"] for record in symbols]
    # MERGE INDEX SYMBOLS
    symbols_list.extend(INDEX_SYMBOLS)

    today = datetime.today().strftime("%Y-%m-%d")

    # for symbol in ["VNM"]:
    for symbol in symbols_list:
        print(f"=== updating quotes for {text_to_red(symbol)}")
        stock_quotes: list[StockQuote] = []

        for interval_index in QuoteInterval:

            interval_name = interval_list[interval_index.value]

            latest_quote = mongodb.get_collection("stock_quotes").find_one(
                filter={"symbol": symbol, "interval": interval_index.value},
                sort={"time": -1},
            )

            if latest_quote:
                last_update_date = datetime.fromtimestamp(
                    latest_quote["time"]
                ).strftime("%Y-%m-%d")
            else:
                last_update_date = "2000-01-01"

            try:
                quotes_df = quoteService.history(
                    symbol=symbol,
                    start=last_update_date,
                    end=today,
                    interval=interval_name,
                )
            except:
                print(
                    text_to_red(f"===== error on {symbol} for interval {interval_name}")
                )
                continue

            # replace NaN with None
            # quotes_df = quotes_df.replace(np.nan, None)

            # drop row that are NaN
            quotes_df.dropna(inplace=True)

            # convert time column to unix timestamp
            quotes_df["time"] = quotes_df["time"].apply(lambda x: int(x.timestamp()))

            # prevent duplicated quotes, e.g. the latest quote could be included
            quotes_df = quotes_df[quotes_df["time"] > latest_quote["time"]]

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

            print(
                f"{text_to_blue(interval_name)} interval has {len(quotes_df)} quotes from {datetime.fromtimestamp(
                    latest_quote["time"]
                ).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )}"
            )

        # insert db
        if len(stock_quotes) > 0:
            stockQuoteRepo.save_many(stock_quotes)
            print(f"{len(stock_quotes)} new quotes for {text_to_red(symbol)} ===")
        else:
            print(f"nothing new for {symbol} ===")

    return len(symbols_list)


if __name__ == "__main__" or __name__ == "tasks":
    main()
