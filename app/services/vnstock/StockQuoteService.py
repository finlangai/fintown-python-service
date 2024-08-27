from pandas import DataFrame
from typing import Union

from app.types import IntervalType
from app.services.vnstock import BaseVnStockService


class StockQuoteService(BaseVnStockService):
    def __init__(
        self,
        symbol: str = "VCI",
        source: str = "VCI",
    ):
        super().__init__(symbol, source)
        self.quote = self.stock.quote

    def history(
        self,
        start: str,
        end: str,
        interval: IntervalType = "1D",
        to_df: bool = True,
        symbol: str = "VCI",
    ) -> Union[DataFrame, dict]:
        """
        Fetch historical stock data for a given symbol.

        Parameters:
        symbol (str): The stock symbol to fetch data for.
        start (str): The start date in 'YYYY-MM-DD' format.
        end (str): The end date in 'YYYY-MM-DD' format.
        interval (str): default 1D or [1m, 5m, 15m, 30m, 1H, 1W, 1M]
        """
        return self.quote.history(
            symbol=symbol, start=start, end=end, interval=interval, to_df=to_df
        )

    def intraday(
        self, symbol: str = "VCI", page_size: int = 100, last_time: str = None
    ) -> DataFrame:
        """
        Parameters:
        symbol (str): The stock symbol to fetch data for.
        page_size (int) Amount of record returned in a single request.
        last_time (str) The last_time date in 'YYYY-MM-DD' format. Specify how far the data should be
        """
        return self.quote.intraday(symbol=symbol, page_size=page_size, last_time=None)
