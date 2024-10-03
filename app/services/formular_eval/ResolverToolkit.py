import pandas as pd
from pandas import DataFrame, Series

from app.models import Parameter
from app.enums import ParamLocation
from app.services.formular_eval import BaseResolver


class ResolverToolkit(BaseResolver):
    def get_column(df: DataFrame, name: str) -> DataFrame:
        return df[name].T.drop_duplicates().T.iloc[:, 0]

    def apply_constraints(self, param: Parameter, df: DataFrame) -> DataFrame:
        """
        Apply constraints to the series
        """
        # check if it should be negative
        if not param.is_allow_negative:
            df = df[param.slug].apply(lambda x: abs(x) if pd.notna(x) else x)

        return df

    def choose_best_column(self, df: DataFrame | Series, name: str) -> DataFrame:
        """
        This function take in the extracted columns for a parameter and return the best one
        *By best one, I mean has the least amount of 0 and NaN
        """
        # return the df if it is a series already
        if isinstance(df, Series):
            df.name = name
            return df.to_frame()

        # Calculate the number of 0s and NaNs in each column
        count_zeros_and_nans = (df.isna() | (df == 0)).sum()

        # Find the index of the column with the minimum number of 0s and NaNs
        best_column_index = count_zeros_and_nans.argmin()

        col: Series = df.iloc[:, best_column_index]
        col.name = name

        return col.to_frame()

    def get_column(self, param: Parameter) -> DataFrame:
        """
        Return the best columns for a field
        """
        df = self.get_data(location=param.location)
        # get the best column
        df = self.choose_best_column(df[param.field], name=param.slug)

        # applying constraints
        df = self.apply_constraints(param=param, df=df)
        return df

    def check_sufficiency(self, parameters: list[Parameter]) -> bool:
        """
        check if the symbol has sufficient parameters to calculate from a formular
        """
        is_sufficient = all(
            param.field in self.get_data(param.location) for param in parameters
        )
        return is_sufficient

    def safe_eval(self, expression: str):
        try:
            return eval(expression)
        except Exception:
            return None

    def get_meta_query(self) -> list:
        """
        Return the query array of metadata e.g. ['yearReport'] or ['yearReport','lengthReport']
        """
        # get the report year and get the length report if is dealing with quarter data
        query_array = ["yearReport"]
        if self.period == "quarter":
            query_array.append("lengthReport")
        return query_array

    def get_meta_df(self) -> DataFrame:
        """
        There should be at least one cache data as this function is called, if not, it gonna get income_statement
        Get the meta dataframe or series e.g. yearReport and lengthReport ( quarter )
        """
        for Param in ParamLocation:
            # not using market price dataframe as base for meta data
            if Param == ParamLocation.market_price:
                continue

            df: DataFrame | None = self.cache.get(Param.name, None)

            # continue if no cache
            if df is None:
                continue

            query_array = self.get_meta_query()

            df = df[query_array]
            break

        # if none of the data was cached, do regression
        if df is None:
            self.get_data(ParamLocation.balance_sheet)
            df = self.get_meta_df()

        return df
