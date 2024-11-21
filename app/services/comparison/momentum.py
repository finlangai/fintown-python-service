import pandas as pd, numpy as np
from datetime import datetime

from app.services import FormularResolver
from app.enums import ParamLocation
from app.models import Formular


class MomentumEdge:
    @staticmethod
    def calculate_delta_percent(df: pd.DataFrame, days):
        df["close_diff"] = df["close"].diff(days)
        df["close_pct_change"] = df["close_diff"] / df["close"].shift(days) * 100
        return df["close_pct_change"].iloc[-1]

    @staticmethod
    def grading(pct: int):
        if pct is np.nan:
            return 0

        # grade 10 if increase 20% or more
        if pct >= 20:
            return 10

        # grade 8 if increase 15% or more
        if pct >= 15:
            return 8

        # grade 6 if increase 10% or more
        if pct >= 10:
            return 6

        # grade 2 if negative
        if pct < 0:
            return 2

        # grade 4 if side way
        return 4

    @staticmethod
    def score_7d(quotes_df: pd.DataFrame):
        """
        Assuming 7d is a week so compare with 5 quote before
        """
        try:
            delta_pct = MomentumEdge.calculate_delta_percent(quotes_df, 5)
            # print("7D: ", delta_pct)
        except:
            return 0

        return MomentumEdge.grading(delta_pct)

    @staticmethod
    def score_30d(quotes_df: pd.DataFrame):
        """
        Assuming 30d is a month so compare with 21 quote before
        """
        try:
            delta_pct = MomentumEdge.calculate_delta_percent(quotes_df, 21)
            # print("30D: ", delta_pct)
        except:
            return 0

        return MomentumEdge.grading(delta_pct)

    @staticmethod
    def score_90d(quotes_df: pd.DataFrame):
        """
        Assuming 90d is 3 three months so compare with 63 quote before
        """
        try:
            delta_pct = MomentumEdge.calculate_delta_percent(quotes_df, 63)
            # print("90D: ", delta_pct)
        except:
            return 0

        return MomentumEdge.grading(delta_pct)

    @staticmethod
    def score_1Y(quotes_df: pd.DataFrame):
        """
        Assuming 1Y is a week so compare with 1 year ago quote before
        """
        try:
            TOTAL_ROW = quotes_df.shape[0]
            delta_pct = MomentumEdge.calculate_delta_percent(quotes_df, TOTAL_ROW - 1)
            print("TOTAL ROWS: ", TOTAL_ROW)
            # print("1Y: ", delta_pct)
        except:
            return 0

        return MomentumEdge.grading(delta_pct)
