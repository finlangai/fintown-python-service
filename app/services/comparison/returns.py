import pandas as pd
from datetime import datetime

from app.services import FormularResolver
from app.enums import ParamLocation
from app.models import Formular


class ReturnsEdge:
    @staticmethod
    def grading_pct(metric_df: pd.DataFrame):
        try:
            TOTAL_ROWS = metric_df.shape[0]
            # grade 10 if the avg growth rate is positive in the previous 5 year
            FIVE_YEARS_OF_QUARTERS = 20
            if (
                TOTAL_ROWS >= FIVE_YEARS_OF_QUARTERS
                and metric_df["pct"].tail(FIVE_YEARS_OF_QUARTERS).mean() > 0
            ):
                return 10

            # grade 8 if the avg growth rate is positive in the previous 3 year
            THREE_YEARS_OF_QUARTERS = 12
            if (
                TOTAL_ROWS >= THREE_YEARS_OF_QUARTERS
                and metric_df["pct"].tail(THREE_YEARS_OF_QUARTERS).mean() > 0
            ):
                return 8

            last_quarter_pct = float(metric_df["pct"].iloc[-1])
            two_Q_before_pct = float(metric_df["pct"].iloc[-2])

            # grade 2 if negative or equal to zero
            if last_quarter_pct <= 0:
                return 2

            # grade 6 if increase but not negative compare to the previous quarter
            if last_quarter_pct > two_Q_before_pct:
                return 6

            # grade 4 if decrease but not negative compare to the previous quarter
            # this is the last case
            return 4
        except:
            return 0

    @staticmethod
    def score_eps(resolver: FormularResolver):
        eps_df = resolver.get_data(location=ParamLocation.metrics)["EPS LTM"]
        eps_df = (
            pd.concat([resolver.get_meta_df(), eps_df], axis=1)
            .iloc[::-1]
            .reset_index(drop=True)
        )

        eps_df["pct"] = eps_df["EPS LTM"].pct_change() * 100

        return ReturnsEdge.grading_pct(eps_df)

    @staticmethod
    def score_roa(resolver: FormularResolver, roa_formular: Formular):
        roa_df = resolver.appraise(roa_formular)
        roa_df = (
            pd.concat([resolver.get_meta_df(), roa_df], axis=1)
            .iloc[::-1]
            .reset_index(drop=True)
        )

        roa_df["pct"] = roa_df[roa_formular.identifier].pct_change() * 100

        return ReturnsEdge.grading_pct(roa_df)

    @staticmethod
    def score_roe(resolver: FormularResolver, roe_formular: Formular):
        roe_df = resolver.appraise(roe_formular)
        roe_df = (
            pd.concat([resolver.get_meta_df(), roe_df], axis=1)
            .iloc[::-1]
            .reset_index(drop=True)
        )

        roe_df["pct"] = roe_df[roe_formular.identifier].pct_change() * 100

        return ReturnsEdge.grading_pct(roe_df)
