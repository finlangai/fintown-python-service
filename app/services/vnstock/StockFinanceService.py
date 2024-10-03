from app.types import PeriodType
from app.services.vnstock import BaseVnStockService

from datetime import datetime
from pandas import DataFrame
from typing import Literal
import pandas as pd


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

    def market_price(self) -> DataFrame:
        """
        Fetch the dataframe for stock closing price quarterly and yearly throughout history
        """
        today = datetime.today().strftime("%Y-%m-%d")

        price_df = self.stock.quote.history(
            symbol=self.symbol,
            start="2000-01-01",
            end=today,
            interval="1D",
            to_df=True,
        )

        # Assuming your dataframe is named df
        price_df["time"] = pd.to_datetime(price_df["time"])
        price_df.set_index("time", inplace=True)

        if self.period == "quarter":
            # Quarterly dataframe
            price_df = price_df.resample("QE").last()

            # set the meta columns
            price_df["yearReport"] = price_df.index.year
            price_df["lengthReport"] = price_df.index.quarter

            # reset index for merging
            price_df.reset_index(inplace=True)

            # take out required columns
            price_df = price_df[["close", "yearReport", "lengthReport"]]
        else:
            # Yearly dataframe
            price_df = price_df.resample("YE").last()

            # set the meta columns
            price_df["yearReport"] = price_df.index.year

            # reset index for merging
            price_df.reset_index(inplace=True)

            # take out required columns
            price_df = price_df[["close", "yearReport"]]

        # rename column close to market price
        price_df.rename(columns={"close": "closed_price"}, inplace=True)

        meta_df = self.get_meta_df()

        price_df = pd.merge(meta_df, price_df, on=self.get_meta_query(), how="left")

        return price_df
