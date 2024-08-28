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
        # return the df if it is a series
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

    def get_meta_df(self) -> DataFrame | None:
        """
        There should be at least one cache data as this function is called
        """
        for Param in ParamLocation:
            df: DataFrame | None = getattr(self, Param.name, None)
            if df is not None:
                # get the report year and get the length report if is dealing with quarter data
                query_array = ["yearReport"]
                if self.period == "quarter":
                    query_array.append("lengthReport")

                df = df[query_array]
                break

        return df
