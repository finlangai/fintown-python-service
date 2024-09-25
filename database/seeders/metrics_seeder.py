import pandas as pd
import numpy as np

from app.utils import print_pink_bold, print_green_bold
from app.services import FormularResolver
from app.models import (
    MetricHistory,
    MetricHistoryRepository,
    CompanyRepository,
    FormularRepository,
)
from app.enums import FormulaType
from app.types import PeriodType


def main():
    print_green_bold("=== SEEDING METRICS")

    # get the list of formulars
    metric_formulars = list(
        FormularRepository().find_by(
            query={"metadata.category": FormulaType.FINANCIAL_METRIC}
        )
    )

    # companies = list(CompanyRepository().find_by(query={"symbol": "vnm"}))
    companies = list(CompanyRepository().find_by(query={}))

    # init resolver
    resolver = FormularResolver(dropna=True)
    timelines = PeriodType.__args__

    # loop through each company
    for c in companies:
        print_pink_bold(f"=== {c.symbol.upper()}")
        resolver.update_symbol(c.symbol)

        # seed quarterly and yearly metrics records for each company
        for period in timelines:
            # change the period of data
            resolver.update_period(period=period)

            # accumulator
            metric_df = pd.DataFrame()
            for metric in metric_formulars:
                metric_df = pd.concat([metric_df, resolver.appraise(metric)], axis=1)

            # Combine metadata and metrics into a MultiIndex DataFrame
            metric_df = pd.concat([resolver.get_meta_df(), metric_df], axis=1)
            metric_df.set_index(resolver.get_meta_query(), inplace=True)

            if period == "quarter":
                records = [
                    MetricHistory(
                        symbol=c.symbol.upper(),
                        year=index[0],
                        quarter=index[1],
                        metrics=row.to_dict(),
                    )
                    for index, row in metric_df.iterrows()
                ]
            else:
                records = [
                    MetricHistory(
                        symbol=c.symbol.upper(),
                        year=index,
                        metrics=row.to_dict(),
                    )
                    for index, row in metric_df.iterrows()
                ]

            MetricHistoryRepository().save_many(models=records)
            print(f"{len(metric_df)} {period}ly records")

    print_green_bold(f"{len(companies)} companies seeded")


if __name__ == "__main__" or __name__ == "tasks":
    main()
