from typing import Literal
from app.services.vnstock import StockFinanceService
from app.types import PeriodType
from app.enums import ParamLocation

from pandas import DataFrame


class BaseResolver(StockFinanceService):
    def get_data(self, location: ParamLocation) -> DataFrame:
        """
        Check if the dataframe of the corresponding symbol on a timeline already exists
        -> yes - return the dataframe
        -> fetch the dataframe -> check if hierachical
        -> yes - flatten
        -> cache
        -> return the dataframe
        """
        location_name = ParamLocation(location).name

        # check if the dataframe already exist
        df: DataFrame | None = self.cache.get(location_name, None)

        # guard
        if df is not None:
            return df

        # call the corresponding function to fetch the dataframe
        df = getattr(self, location_name)()

        # check if is hierachical to get second level ( dealing with ratio data)
        if df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(1)

        # caching
        self.cache[location_name] = df

        return df

    def clean_cached_data(self) -> None:
        """
        clean cached dataframes
        """
        self.cache.clear()

    def update_symbol(self, symbol: str):
        super().update_symbol(symbol)
        self.clean_cached_data()

    def update_period(self, period: PeriodType):
        super().update_period(period)
        self.clean_cached_data()
