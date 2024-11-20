import pandas as pd
from datetime import datetime

from app.services import FormularResolver
from app.enums import ParamLocation
from app.models import Formular


class RevenueProfitEdge:
    @staticmethod
    def scrore_profit(resolver: FormularResolver, profit_growth_formular: Formular):
        try:
            profit_gr_df = resolver.appraise(profit_growth_formular)
            profit_gr_df = (
                pd.concat([resolver.get_meta_df(), profit_gr_df], axis=1)
                .iloc[::-1]
                .reset_index(drop=True)
            )

            TOTAL_GROWTH = profit_gr_df.shape[0]

            # grade 10 if last 5 years have avg above 20%
            if (
                TOTAL_GROWTH >= 20
                and profit_gr_df["net_profit_growth_rate"].tail(20).mean() >= 20
            ):
                return 10

            # grade 8 if last 3 years have avg above 20%
            if (
                TOTAL_GROWTH >= 12
                and profit_gr_df["net_profit_growth_rate"].tail(12).mean() >= 20
            ):
                return 8

            last_quarter_rate = float(profit_gr_df.iloc[-1]["net_profit_growth_rate"])
            # grade 6 if growth more than 20% compare to last quarter
            if last_quarter_rate >= 20:
                return 6

            # grade 2 if negative or equal to 0
            if last_quarter_rate <= 0:
                return 2

            # grade 4 if only positive
            return 4
        except:
            return 0

    @staticmethod
    def scrore_revenue(resolver: FormularResolver, revenue_growth_formular: Formular):
        try:
            revenue_gr_df = resolver.appraise(revenue_growth_formular)
            revenue_gr_df = (
                pd.concat([resolver.get_meta_df(), revenue_gr_df], axis=1)
                .iloc[::-1]
                .reset_index(drop=True)
            )

            TOTAL_ROW = revenue_gr_df.shape[0]

            # grade 10 if last 5 years have avg above 10%
            if (
                TOTAL_ROW >= 20
                and revenue_gr_df[revenue_growth_formular.identifier].tail(20).mean()
                >= 10
            ):
                return 10

            # grade 8 if last 3 years have avg above 10%
            if (
                TOTAL_ROW >= 12
                and revenue_gr_df[revenue_growth_formular.identifier].tail(12).mean()
                >= 10
            ):
                return 8

            last_quarter_rate = float(
                revenue_gr_df.iloc[-1][revenue_growth_formular.identifier]
            )

            # grade 6 if growth more than 10% compare to last quarter
            if last_quarter_rate >= 10:
                return 6

            # grade 2 if negative or equal to 0
            if last_quarter_rate <= 0:
                return 2

            # grade 4 if only positive
            return 4
        except:
            return 0

    @staticmethod
    def scrore_npm(resolver: FormularResolver, npm_growth_formular: Formular):
        try:
            npm_df = resolver.appraise(npm_growth_formular)
            npm_df = (
                pd.concat([resolver.get_meta_df(), npm_df], axis=1)
                .iloc[::-1]
                .reset_index(drop=True)
            )

            TOTAL_ROW = npm_df.shape[0]
            npm_df["pct"] = npm_df[npm_growth_formular.identifier].pct_change() * 100

            # grade 10 if last 5 years have avg above 5%
            if TOTAL_ROW >= 20 and npm_df["pct"].tail(20).mean() >= 5:
                return 10

            # grade 8 if last 3 years have avg above 5%
            if TOTAL_ROW >= 12 and npm_df["pct"].tail(12).mean() >= 5:
                return 8

            last_quarter_rate = float(npm_df.iloc[-1]["pct"])

            # grade 6 if growth more than 5% compare to last quarter
            if last_quarter_rate >= 5:
                return 6

            # grade 2 if negative or equal to 0
            if last_quarter_rate <= 0:
                return 2

            # grade 4 if only positive
            return 4
        except:
            return 0
