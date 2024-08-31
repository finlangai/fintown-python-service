from app.utils import print_pink_bold, print_green_bold
from app.models import (
    CompanyRepository,
    MetricHistoryRepository,
    Assessment,
    Forecasted,
    AssessmentRepository,
)
from app.services.forecasting import LinearRegressionForecaster
from core import mongodb
import pandas as pd
import numpy as np
from datetime import datetime


def main():
    print("Assessment Seeder")
    # companies = list(CompanyRepository().find_by(query={"_id": "MBB"}))
    companies = list(CompanyRepository().find_by(query={}))

    forecaster = LinearRegressionForecaster()
    assessmentRepo = AssessmentRepository()
    for c in companies:
        print_pink_bold(f"=== {c.id}")
        # assessment = Assessment(symbol=c.id)

        history = mongodb.query_with_projection(
            collection_name=MetricHistoryRepository.Meta.collection_name,
            query={"symbol": c.id, "quarter": 0},
            projection={"_id": 0, "year": 1, "metrics": 1},
        )

        df = pd.json_normalize(data=history)

        df.set_index("year", inplace=True)
        df.sort_index(ascending=True, inplace=True)

        df.columns = [col.replace("metrics.", "") for col in df.columns]

        highest_index = df.index.max()
        acc_df = pd.DataFrame()
        for col_name in df.columns:
            forecaster.reset()

            series = df[col_name].dropna()
            years_2d = series.index.values.reshape(-1, 1)
            targets_1d = series.values

            forecaster.train(X_2d=years_2d, y_1d=targets_1d)
            futures = np.array(range(highest_index + 1, highest_index + 6))

            result = forecaster.forecast(X_2d=futures.reshape(-1, 1))
            result = pd.Series(data=result, index=futures)
            result.name = col_name
            acc_df = pd.concat([acc_df, result], axis=1)

        forecasted_list: list[Forecasted] = []
        for index, row in acc_df.iterrows():
            metrics: dict = {}
            for col_name in acc_df.columns:
                metrics[col_name] = row[col_name]
            forecasted_list.append(Forecasted(year=index, metrics=metrics))

        assessment = Assessment(
            symbol=c.id, updated_year=datetime.now().year, forecasts=forecasted_list
        )
        assessmentRepo.save(model=assessment)


if __name__ == "__main__" or __name__ == "tasks":
    main()
