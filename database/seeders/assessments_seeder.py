from app.utils import print_pink_bold, print_green_bold
from app.models import (
    CompanyRepository,
    Assessment,
    AssessmentRepository,
    MetricHistoryRepository,
    ForecastedMetric,
    QuarterlyAssessment,
    YearlyAssessment,
)
from app.services.forecasting import LinearRegressionForecaster
from core import mongodb
import pandas as pd
import numpy as np


def main():
    print("Assessment Seeder")
    # companies = list(CompanyRepository().find_by(query={"_id": "MBB"}))
    companies = list(CompanyRepository().find_by(query={}))
    timelines = [
        {
            "name": "quarterly",
            "query": {"quarter": {"$ne": 0}},
            "projection": {"quarter": 1},
            "indexes": "continuous",
            "futures": "np.arange(highest_index + 0.25, highest_index + 1.5, 0.25)",
        },
        {
            "name": "yearly",
            "query": {"quarter": 0},
            "projection": {},
            "indexes": "year",
            "futures": "range(highest_index + 1, highest_index + 6)",
        },
    ]

    forecaster = LinearRegressionForecaster()
    assessmentRepo = AssessmentRepository()
    for c in companies:
        print_pink_bold(f"=== {c.id}")
        # assessment = Assessment(symbol=c.id)

        for period in timelines:

            history = mongodb.query_with_projection(
                collection_name=MetricHistoryRepository.Meta.collection_name,
                query={"symbol": c.id, **period["query"]},
                projection={"_id": 0, "year": 1, "metrics": 1, **period["projection"]},
            )

            df = pd.json_normalize(data=history)

            if period["name"] == "quarterly":
                df["continuous"] = df["year"] + df["quarter"] / 4

            df.set_index(period["indexes"], inplace=True)
            df.sort_index(ascending=True, inplace=True)

            df.columns = [col.replace("metrics.", "") for col in df.columns]

            highest_index = df.index.max()
            acc_df = pd.DataFrame()
            for col_name in df.columns:
                if col_name in ["year", "quarter"]:
                    continue
                forecaster.reset()

                series = df[col_name].dropna()
                years_2d = series.index.values.reshape(-1, 1)
                targets_1d = series.values

                forecaster.train(X_2d=years_2d, y_1d=targets_1d)
                futures = np.array(eval(period["futures"]))

                result = forecaster.forecast(X_2d=futures.reshape(-1, 1))
                result = pd.Series(data=result, index=futures)
                result.name = col_name
                acc_df = pd.concat([acc_df, result], axis=1)

            if period["name"] == "quarterly":
                acc_df["year"] = acc_df.index.astype(int)
                acc_df["quarter"] = ((acc_df.index - acc_df["year"]) * 4).astype(int)

                # Replacing rows where quarter is 0 with quarter = 4 and decrementing the year by 1
                acc_df.loc[acc_df["quarter"] == 0, "quarter"] = 4
                acc_df.loc[acc_df["quarter"] == 4, "year"] -= 1

                acc_df.set_index(["year", "quarter"], inplace=True)

                quarterly_forecasts: dict = {}
                for col_name in acc_df.columns:
                    forecasted_arr: list[ForecastedMetric] = []
                    series: pd.DataFrame = acc_df[col_name].to_frame()

                    for idx, row in series.iterrows():
                        point = ForecastedMetric(
                            year=idx[0], quarter=idx[1], value=row[col_name]
                        )
                        forecasted_arr.append(point)
                    quarterly_forecasts[col_name] = forecasted_arr

                quarterlyAssessment = QuarterlyAssessment(forecasts=quarterly_forecasts)
                continue
            # yearly
            yearly_forecasts: dict = {}
            for col_name in acc_df.columns:
                forecasted_arr: list[ForecastedMetric] = []
                series: pd.DataFrame = acc_df[col_name].to_frame()

                for idx, row in series.iterrows():
                    point = ForecastedMetric(year=idx, value=row[col_name])
                    forecasted_arr.append(point)
                yearly_forecasts[col_name] = forecasted_arr
            yearlyAssessment = YearlyAssessment(forecasts=yearly_forecasts)
        assessment = Assessment(
            symbol=c.id, quarterly=quarterlyAssessment, yearly=yearlyAssessment
        )
        assessmentRepo.save(model=assessment)


if __name__ == "__main__" or __name__ == "tasks":
    main()
