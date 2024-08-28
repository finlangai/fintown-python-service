import pandas as pd
import numpy as np

from app.utils import print_pink_bold
from app.services import FormularResolver
from app.models import (
    MetricHistory,
    MetricHistoryRepository,
    CompanyRepository,
    FormulaRepository,
)
from app.enums import FormulaType


def main():
    print("Metrics seeder")
    FormulaRepo = FormulaRepository()
    metric_formulars = list(
        FormulaRepo.find_by(query={"category": FormulaType.FINANCIAL_METRIC})
    )

    CompanyRepo = CompanyRepository()
    # companies = list(CompanyRepo.find_by(query={"_id": "vnm"}))
    companies = list(CompanyRepo.find_by(query={}))

    resolver = FormularResolver(dropna=True)
    for c in companies:
        print_pink_bold(f"=== {c.id.upper()}")
        resolver.update_symbol(c.id)
        metric_df = pd.DataFrame()
        for metric in metric_formulars:
            metric_df = pd.concat([metric_df, resolver.appraise(metric)], axis=1)

        # Combine metadata and metrics into a MultiIndex DataFrame
        metric_df = pd.concat([resolver.get_meta_df(), metric_df], axis=1)
        metric_df.set_index(["yearReport", "lengthReport"], inplace=True)

        records = [
            MetricHistory(
                symbol=c.id.upper(),
                year=index[0],
                quarter=index[1],
                metrics=row.to_dict(),
            )
            for index, row in metric_df.iterrows()
        ]

        MetricHistoryRepository().save_many(models=records)
        print(f"{len(metric_df)} quarter records")


if __name__ == "__main__" or __name__ == "tasks":
    main()
