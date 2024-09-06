import pandas as pd
import numpy as np
from datetime import datetime
from core import mongodb

from app.utils import print_pink_bold, print_green_bold
from app.models import (
    CompanyRepository,
    MetricHistoryRepository,
    Assessment,
    Forecasted,
    AssessmentRepository,
    FormularRepository,
)
from app.services.forecasting import LinearRegressionForecaster
from app.enums import FormulaType


def main():
    print("Assessment Seeder")
    companies = list(CompanyRepository().find_by(query={"_id": "MBB"}))
    # companies = list(CompanyRepository().find_by(query={}))

    forecaster = LinearRegressionForecaster()

    assessmentRepo = AssessmentRepository()
    formulars_dict = {
        f.identifier: f
        for f in list(
            FormularRepository().find_by(
                query={"metadata.category": FormulaType.FINANCIAL_METRIC}
            )
        )
    }

    for c in companies:
        print_pink_bold(f"=== {c.id}")
        # === INNER

        history = mongodb.query_with_projection(
            collection_name=MetricHistoryRepository.Meta.collection_name,
            query={"symbol": c.id, "quarter": 0},
            projection={"_id": 0, "year": 1, "metrics": 1},
        )

        df = forecaster.prepare_dataframe(raw=history)

        acc_df = pd.DataFrame()

        for col_name in df.columns:

            # get the corresponding metric series and remove invalid rows
            series = forecaster.polish_series(df, col_name)

            forecasted = forecaster.forecast(initial=series, years_ahead=5)
            acc_df = pd.concat([acc_df, forecasted], axis=1)

        print(acc_df)

        import sys

        sys.exit()
        # forecasted metrics for 5 years ahead
        forecasted_list: list[Forecasted] = []

        for index, row in acc_df.iterrows():
            metrics: dict = {}
            for col_name in acc_df.columns:
                metrics[col_name] = row[col_name]
            forecasted_list.append(Forecasted(year=index, metrics=metrics))

        assessment = Assessment(
            symbol=c.id, updated_year=datetime.now().year, forecasts=forecasted_list
        )
        # assessmentRepo.save(model=assessment)


if __name__ == "__main__" or __name__ == "tasks":
    main()
