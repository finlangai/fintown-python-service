from app.services.vnstock import StockFinanceService
from app.types import PeriodType
from app.enums import ParamLocation

from pandas import DataFrame


class BaseResolver(StockFinanceService):
    def get_data(self, location: ParamLocation) -> DataFrame:
        """
        Check if the dataframe of the corresponding symbol on a timeline already exists
        -> yes - return the dataframe
        -> no - fetch the dataframe then set and return
        """
        location_name = ParamLocation(location).name

        # check if the dataframe already exist
        df = getattr(self, location_name, None)

        if df is not None:
            return df

        # fetch the dataframe
        df = getattr(self.finance, location_name)()
        # caching
        setattr(self, location_name, df)

        return df

    def clean_finance_data(self) -> None:
        """
        clean cached dataframes
        """
        self.ratio = None
        self.balance_sheet = None
        self.income_statement = None
        self.cash_flow = None

    def update_symbol(self, symbol: str):
        super().update_symbol(symbol)
        self.clean_finance_data()

    def update_period(self, period: PeriodType):
        super().update_period(period)
        self.clean_finance_data()
