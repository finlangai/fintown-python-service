import numpy as np
import pandas as pd


class ForecastingToolkit:
    def __init__(self):
        pass

    def prepare_dataframe(self, raw: list[dict]) -> pd.DataFrame:
        """
        Prepare appropriate dataframe from metrics data which is a list of dicts retrieve from database
        """

        df = pd.json_normalize(data=raw)

        df.set_index("year", inplace=True)
        df.sort_index(ascending=True, inplace=True)

        df.columns = [col.replace("metrics.", "") for col in df.columns]

        return df

    def polish_series(self, df: pd.DataFrame, col_name: str):
        """
        Select the desired column and remove invalid rows
        """
        return df[col_name].dropna()
