import pandas as pd, numpy as np, sys
from datetime import datetime
from core import mongodb

from app.utils import (
    print_pink_bold,
    print_green_bold,
    text_to_red,
    text_to_italic,
    text_to_blue,
)
from app.services import LinearRegressionForecaster, BaseLLMService
from app.enums import FormulaType
from app.models import (
    CompanyRepository,
    MetricHistoryRepository,
    FormularRepository,
)
from app.models.Assessment import (
    Assessment,
    Forecasted,
    Insights,
    Cluster,
    Criteria,
    AssessmentRepository,
)
from config.assessment import criterias
from config.llm.prompts import (
    cluster_review_prompt,
    metric_input_template,
    status_prompt,
    thesis_input_template,
    criteria_thesis_prompt,
    overall_prompt,
    overall_input_template,
)


def main():
    print_green_bold("Assessment Seeder")
    # companies = list(CompanyRepository().find_by(query={"symbol": "MBB"}))
    # companies = list(CompanyRepository().find_by(query={}))

    forecaster = LinearRegressionForecaster()
    llm = BaseLLMService()

    assessmentRepo = AssessmentRepository()

    # get the list of formulars and have it as a dict to query with identifier
    formulars_dict = {
        f.identifier: f
        for f in list(
            FormularRepository().find_by(
                query={"metadata.category": FormulaType.FINANCIAL_METRIC}
            )
        )
    }

    # get all metrics required in all criterias
    required_metrics_identifiers = []
    for criteria in criterias:
        for group in criteria["groups"]:
            required_metrics_identifiers.extend(group["metrics"])

    # LOOP THROUGH EACH COMPANY
    for symbol in ["VNM"]:
        print_pink_bold(f"=== {symbol}")

        # ======================================
        # ===== PREPARE METRICS DATAFRAME ======
        # ======================================
        history = mongodb.query_with_projection(
            collection_name=MetricHistoryRepository.Meta.collection_name,
            query={"symbol": symbol, "quarter": 0},
            projection={"_id": 0, "year": 1, "metrics": 1},
        )

        metrics_df: pd.DataFrame = forecaster.prepare_dataframe(raw=history)
        # drop all un required columns
        for column_name in metrics_df:
            if column_name not in required_metrics_identifiers:
                metrics_df.drop(column_name, axis=1, inplace=True)

        # round to two digit
        metrics_df = metrics_df.round(2)
        # ======================================================
        # ===== FORECAST 5 YEARS FOR ALL REQUIRED METRICS ======
        # ======================================================
        forecasted_df = pd.DataFrame()

        # loop through each column in the prepared dataframe
        for col_name in metrics_df.columns:
            print(
                text_to_red(f"forecasting")
                + " "
                + text_to_italic(formulars_dict[col_name].name)
            )
            # get the corresponding metric series and remove invalid rows
            series = forecaster.polish_series(metrics_df, col_name)

            # pass in the series of the corresponding metric then forecast the next 5 years
            forecasted: pd.Series = forecaster.forecast(initial=series, years_ahead=5)

            forecasted_df = pd.concat([forecasted_df, forecasted], axis=1)

        # round to two digit
        forecasted_df = forecasted_df.round(2)
        # ===================================================
        # ======= ASSESSMENT & STATUS FOR EACH GROUP ========
        # ===================================================
        # storing result
        criterias_holder: list[Criteria] = []

        print(text_to_blue(f"====== APPRAISING CRITERIAS ======"))
        for criteria in criterias:
            print(f"=== Criteria {criteria['criteria_name']}")
            groups: list = criteria["groups"]
            clusters_holder: list[Cluster] = []
            # ===========================================================
            # ====== GENERATE ASSESSMENT & STATUS FOR EACH CLUSTER ======
            # ===========================================================
            # loop through each cluster
            for cluster in groups:
                print(f"- group {cluster['cluster_name']}")
                metrics_data = ""
                cluster_metric_identifiers = []
                # map the metrics data for prompting
                for identifier in cluster["metrics"]:
                    # if the required metrics not present on this symbol, skip
                    if identifier not in metrics_df:
                        continue
                    # get the metric info from the dict
                    metric_info = formulars_dict[identifier]
                    # concat to the metrics_data
                    metrics_data += metric_input_template.format(
                        metric_name=metric_info.name,
                        metric_name_vi=metric_info.name_vi,
                        historical_data=metrics_df[identifier].to_string(),
                        forecasted_data=forecasted_df[identifier].to_string(),
                    )
                    # push the index of the metric into metric_indexes for defining cluster later
                    cluster_metric_identifiers.append(metric_info.identifier)

                # create prompt for cluster assessment
                prompt_for_cluster = cluster_review_prompt.format(
                    metrics_data=metrics_data,
                    metric_cluster_name=cluster["cluster_name"],
                    symbol=symbol,
                )
                # invoking the llm for assessment
                cluster_assessment = llm.invoke(prompt_for_cluster)

                # create prompt for cluster status
                cluster_status_prompt = status_prompt.format(
                    assessment=cluster_assessment
                )
                # invoking the llm for status
                cluster_status = llm.invoke(cluster_status_prompt)
                # push new cluster to the list
                clusters_holder.append(
                    Cluster(
                        assessment=cluster_assessment,
                        status=cluster_status,
                        metrics=cluster_metric_identifiers,
                    )
                )
            # =======================================================
            # ====== GENERATE ASSESSMENT & STATUS FOR CRITERIA ======
            # =======================================================
            thesis_input = ""
            # loop through each cluster to generate thesis_input
            for index, cluster in enumerate(clusters_holder):
                thesis_input += thesis_input_template.format(
                    cluster_name=groups[index]["cluster_name"],
                    status=cluster.status,
                    review=cluster.assessment,
                )
            # create prompt for criteria thesis
            criteria_prompt = criteria_thesis_prompt.format(
                criteria_name=criteria["criteria_name"],
                symbol=symbol,
                thesis_input=thesis_input,
            )
            # invoke the llm for assessment
            criteria_assessment = llm.invoke(criteria_prompt)
            # create prompt for status
            criteria_status_prompt = status_prompt.format(
                assessment=criteria_assessment
            )
            # invoke the llm for status
            criteria_status = llm.invoke(criteria_status_prompt)
            # set the criteria to the holder
            criterias_holder.append(
                Criteria(
                    assessment=criteria_assessment,
                    status=criteria_status,
                    groups=clusters_holder,
                )
            )
        # =====================================================
        # ============ GENERATE OVERALL ASSESSMENT ============
        # =====================================================
        # loop through and generate overall input
        overall_input = ""
        for index, criteria in enumerate(criterias_holder):
            overall_input += overall_input_template.format(
                criteria_name=criterias[index]["criteria_name"],
                status=criteria.status,
                assessment=criteria.assessment,
            )
        # create prompt for overall assessment
        overall_assessment_prompt = overall_prompt.format(
            symbol=symbol, overall_input=overall_input
        )
        # invoke the llm for overall assessment
        overall_assessment = llm.invoke(overall_assessment_prompt)
        # ==============================================
        # ============ CREATE FINAL MODEL ============
        # ==============================================
        insights = Insights(
            overall=overall_assessment,
            profitability=criterias_holder[0],
            solvency=criterias_holder[1],
            revenue_profit=criterias_holder[2],
            assets_cashflow=criterias_holder[3],
            assets_equity=criterias_holder[4],
        )

        forecasted_list = forecasted_df.apply(
            lambda row: {"year": row.name, "metrics": row.to_dict()}, axis=1
        ).tolist()
        # calculate the future delta for each metrics
        deltas: dict[str, float] = {}
        for identifier in forecasted_df.columns:
            inital = metrics_df.iloc[-1][identifier]
            farthest = forecasted_df.iloc[-1][identifier]
            delta = (farthest - inital) / inital
            deltas[identifier] = delta

        final_model = Assessment(
            symbol=symbol,
            forecast=forecasted_list,
            future_deltas=deltas,
            insights=insights,
        )
        # save the record
        assessmentRepo.save(final_model)


if __name__ == "__main__" or __name__ == "tasks":
    main()
