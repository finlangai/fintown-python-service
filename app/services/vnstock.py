from vnstock3 import Vnstock
from pandas import DataFrame
from typing import Union, Literal, TypeAlias


SoureType: TypeAlias = Literal["TCBS", "VCI"]


class BaseVnStockService:
    def __init__(self, symbol: str = "VCI", source: SoureType = "TCBS"):
        self.stock = Vnstock().stock(symbol=symbol, source=source)


class StockInfoService(BaseVnStockService):
    def __init__(self, symbol: str = "VCI", source: SoureType = "TCBS"):
        super().__init__(symbol, source)
        self.company = self.stock.company

    def overview(self) -> DataFrame:
        return self.company.overview()

    def profile(self) -> DataFrame:
        return self.company.profile()

    def subsidiaries(self) -> DataFrame:
        return self.company.subsidiaries()

    def events(self) -> DataFrame:
        return self.company.events()

    def news(self) -> DataFrame:
        return self.company.news()


PeriodType: TypeAlias = Literal["quarter", "year"]


class StockFinanceService(BaseVnStockService):
    def __init__(
        self,
        symbol: str = "VCI",
        source: str = "VCI",
        lang: Literal["en", "vi"] = "en",
        dropna: bool = False,
    ):
        super().__init__(symbol, source)
        self.finance = self.stock.finance
        self.lang = lang
        self.dropna = dropna

    def income_statement(
        self, symbol: str = "VCI", period: PeriodType = "quarter"
    ) -> DataFrame:
        return self.finance.income_statement(
            symbol=symbol, period=period, lang=self.lang, dropna=self.dropna
        )

    def balance_sheet(
        self, symbol: str = "VCI", period: PeriodType = "quarter"
    ) -> DataFrame:
        return self.finance.balance_sheet(
            symbol=symbol, period=period, lang=self.lang, dropna=self.dropna
        )

    def cash_flow(
        self, symbol: str = "VCI", period: PeriodType = "quarter"
    ) -> DataFrame:
        return self.finance.cash_flow(
            symbol=symbol, period=period, lang=self.lang, dropna=self.dropna
        )

    def ratio(self, symbol: str = "VCI", period: PeriodType = "quarter") -> DataFrame:
        return self.finance.ratio(
            symbol=symbol,
            period=period,
            lang=self.lang,
            dropna=self.dropna,
        )


IntervalType: TypeAlias = Literal["1m", "5m", "15m", "30m", "1H", "1D", "1W", "1M"]


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
