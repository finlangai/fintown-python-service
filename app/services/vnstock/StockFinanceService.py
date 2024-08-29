from pandas import DataFrame
from typing import Literal

from app.types import PeriodType
from app.services.vnstock import BaseVnStockService


class StockFinanceService(BaseVnStockService):
    def __init__(
        self,
        symbol: str = "VCI",
        source: str = "VCI",
        lang: Literal["en", "vi"] = "en",
        dropna: bool = False,
        period: PeriodType = "quarter",
    ):
        super().__init__(symbol, source)
        self.finance = self.stock.finance
        self.lang = lang
        self.dropna = dropna
        self.period = period
        self.cache = dict()

    def update_symbol(self, symbol: str):
        """
        Update the symbol when fetching data
        """
        self.symbol = symbol.upper()
        self.finance._update_data_source(symbol=symbol)

    def update_period(self, period: PeriodType):
        """
        Update the period when fetching data
        """
        self.period = period

    def income_statement(self) -> DataFrame:
        """
        Fetch the dataframe for income statements throughout history
        """
        return self.finance.income_statement(
            period=self.period, lang=self.lang, dropna=self.dropna
        )

    def balance_sheet(self) -> DataFrame:
        """
        Fetch the dataframe for balance sheets throughout history
        """
        return self.finance.balance_sheet(
            period=self.period, lang=self.lang, dropna=self.dropna
        )

    def cash_flow(self) -> DataFrame:
        """
        Fetch the dataframe for cashflow statements throughout history
        """
        return self.finance.cash_flow(
            period=self.period, lang=self.lang, dropna=self.dropna
        )

    def ratio(self) -> DataFrame:
        """
        Fetch the dataframe for ratio data throughout history
        """
        return self.finance.ratio(
            period=self.period,
            lang=self.lang,
            dropna=self.dropna,
        )
