import sys
import pandas as pd
import numpy as np
from datetime import datetime
from core import mongodb

from app.utils import (
    print_pink_bold,
    print_green_bold,
    text_to_red,
    text_to_blue,
    text_to_italic,
)
from app.models import (
    CompanyRepository,
    MetricHistoryRepository,
    Assessment,
    Forecasted,
    AssessmentRepository,
    FormularRepository,
)
from app.services.forecasting import LinearRegressionForecaster
from app.services.llm import FinanceAppraiser
from app.enums import FormulaType


def main():
    print_green_bold("Assessment Seeder")
    # companies = list(CompanyRepository().find_by(query={"symbol": "MBB"}))
    companies = list(CompanyRepository().find_by(query={}))

    forecaster = LinearRegressionForecaster()
    appraiser = FinanceAppraiser()

    assessmentRepo = AssessmentRepository()
    metricRepo = MetricHistoryRepository()

    # get the list of formulars
    formulars_dict = {
        f.identifier: f
        for f in list(
            FormularRepository().find_by(
                query={"metadata.category": FormulaType.FINANCIAL_METRIC}
            )
        )
    }

    # LOOP THROUGH EACH COMPANY
    for c in companies:
        print_pink_bold(f"=== {c.symbol}")
        # === INNER

        history = mongodb.query_with_projection(
            collection_name=MetricHistoryRepository.Meta.collection_name,
            query={"symbol": c.symbol, "quarter": 0},
            projection={"_id": 0, "year": 1, "metrics": 1},
        )

        df: pd.DataFrame = forecaster.prepare_dataframe(raw=history)

        acc_df = pd.DataFrame()

        insights = {}
        metric_histories = list(
            metricRepo.find_by(
                {"symbol": c.symbol, "quarter": 0}, sort=[("year", -1)], limit=5
            )
        )
        print(f"{len(metric_histories[0].metrics)} metrics")

        # loop through each column in the prepared dataframe
        for col_name in df.columns:
            print(
                text_to_red(f"appraising")
                + " "
                + text_to_italic(formulars_dict[col_name].name)
            )
            # get the corresponding metric series and remove invalid rows
            series = forecaster.polish_series(df, col_name)

            # pass in the series of the corresponding metric then forecast the next 5 years
            forecasted: pd.Series = forecaster.forecast(initial=series, years_ahead=5)

            acc_df = pd.concat([acc_df, forecasted], axis=1)

            history = [
                {"year": period.year, col_name: period.metrics[col_name]}
                for period in metric_histories
            ]

            result: dict | None = None

            while result is None:
                response = appraiser.appraise(
                    symbol=c.symbol,
                    name=c.company_name,
                    forecast=forecasted.to_csv(),
                    industry=c.industry,
                    metric_info=formulars_dict[col_name].description,
                    metric_histories=history,
                )
                result = appraiser.validate_response(res=response)

            insights[col_name] = result

        # MAP FORECASTED DATA INTO A LIST

        forecasted_list: list[Forecasted] = []

        # Loop through and push Forecasted object into the forecasted_list
        for index, row in acc_df.iterrows():
            metrics: dict = {}
            for col_name in acc_df.columns:
                metrics[col_name] = row[col_name]
            forecasted_list.append(Forecasted(year=index, metrics=metrics))

        assessment = Assessment(
            symbol=c.symbol,
            updated_year=datetime.now().year,
            forecasts=forecasted_list,
            insights=insights,
        )
        assessmentRepo.save(model=assessment)


if __name__ == "__main__" or __name__ == "tasks":
    main()
