import pandas as pd, numpy as np, sys
from datetime import datetime
from core import mongodb

from app.services import (
    LinearRegressionForecaster,
    BaseLLMService,
    PromptHelper,
    DatabaseResources,
)
from app.enums import FormulaType
from app.utils import (
    print_pink_bold,
    print_green_bold,
    text_to_red,
    text_to_italic,
    text_to_blue,
)
from app.models import (
    MetricHistoryRepository,
    FormularRepository,
    Assessment,
    AssessmentCluster,
    AssessmentCriteria,
    AssessmentRepository,
    CriteriaRepository,
    CriteriaCluster,
)
from config.llm.prompts import status_prompt
from config.seeder import STOCK_SYMBOLS


def main(custom_symbol: str = None):
    """
    Depend on criteria seeder
    """
    print_green_bold("=== Assessments Seeder")
    # ====================================================
    # ======= CONFIG SYMBOL TO SEED ASSESSMENT FOR =======
    # ====================================================
    # symbol_list = STOCK_SYMBOLS
    symbol_list = ["VCB"]
    if custom_symbol is not None:
        symbol_list = [custom_symbol]

    # ====================================================
    # ============= PREPARE REQUIRED SERVICE =============
    # ====================================================

    llm = BaseLLMService()
    forecaster = LinearRegressionForecaster()
    assessmentRepo = AssessmentRepository()

    # get the list of criterias
    criterias_list = DatabaseResources.criterias_list()
    # get the list of formulars and have it as a dict to query with identifier
    formulars_dict = DatabaseResources.formulars_dict()

    # get all metrics required in all criterias
    required_metrics_identifiers = []
    for criteria in criterias_list:
        for group in criteria.group:
            required_metrics_identifiers.extend(group.metrics)

    # LOOP THROUGH EACH COMPANY
    for symbol in symbol_list:
        # for symbol in STOCK_SYMBOLS:
        print_pink_bold(f"=== {symbol}")
        # ======================================
        # ===== PREPARE METRICS DATAFRAME ======
        # ======================================
        history = mongodb.query_with_projection(
            collection_name=MetricHistoryRepository.Meta.collection_name,
            query={"symbol": symbol, "quarter": 0},
            projection={"_id": 0, "year": 1, "metrics": 1},
        )

        # PREPARE THE METRICS DATAFRAME OF THE SYMBOL FROM METRIC_RECORDS COLLECTION
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

        print(text_to_red(f"forecast {len(metrics_df.columns)} metrics"))
        # loop through each column in the prepared dataframe
        for col_name in metrics_df.columns:
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
        criterias_holder: list[AssessmentCriteria] = []

        print_green_bold("====== ASSESSING CRITERIAS ======")
        for criteria in criterias_list:
            print(f"=== Criteria {criteria.name}")
            # group of cluster in config file
            group: list[CriteriaCluster] = criteria.group
            clusters_holder: list[AssessmentCluster] = []

            # ====================================================================
            # ====== GENERATE ASSESSMENT & STATUS FOR EACH GROUP OR CLUSTER ======
            # ====================================================================
            # loop through each cluster
            for cluster in group:
                print(f"- cluster {cluster.name}")
                # check if the symbol has at least one metric present in the cluster
                is_metric_present = set(cluster.metrics).intersection(
                    metrics_df.columns
                )
                if not is_metric_present:
                    print(f"{text_to_italic(f"{text_to_red("not")} present")}")
                    clusters_holder.append(None)
                    continue

                # get the list of appraisable metric identifiers in the cluster
                cluster_metric_identifiers = [
                    formulars_dict[identifier].identifier
                    for identifier in cluster.metrics
                    if identifier in metrics_df
                ]

                # create prompt for cluster assessment
                prompt_for_cluster = PromptHelper.craft_cluster(
                    symbol=symbol,
                    cluster=cluster,
                    metrics_df=metrics_df,
                    forecasted_df=forecasted_df,
                    formulars_dict=formulars_dict,
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
                    AssessmentCluster(
                        assessment=cluster_assessment,
                        status=cluster_status,
                        metrics=cluster_metric_identifiers,
                    )
                )
                print(f"{text_to_italic("present")}")

            # =======================================================
            # ====== GENERATE ASSESSMENT & STATUS FOR CRITERIA ======
            # =======================================================
            print(f"{text_to_blue(f"= Assessing criteria {criteria.name}")}")
            criteria_prompt = PromptHelper.craft_criteria(
                symbol=symbol,
                criteria_name=criteria.name,
                clusters_holder=clusters_holder,
                group=group,
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
                AssessmentCriteria(
                    assessment=criteria_assessment,
                    status=criteria_status,
                    groups=clusters_holder,
                )
            )
        # =====================================================
        # ============ GENERATE OVERALL ASSESSMENT ============
        # =====================================================
        print(
            f"{text_to_red(f"= Assessing Overall base on {len(criterias_list)} criterias")}"
        )

        overall_assessment_prompt = PromptHelper.craft_overall(
            symbol=symbol,
            criterias_holder=criterias_holder,
            criterias_list=criterias_list,
        )
        # invoke the llm for overall assessment
        overall_assessment = llm.invoke(overall_assessment_prompt)

        # ==============================================
        # ============ CREATE FINAL MODEL ==============
        # ==============================================
        print(f"{text_to_red(f"= Creating final model")}")
        insights = dict()
        insights.update({"overall": overall_assessment})
        # update into the dict
        for index, criteria in enumerate(criterias_list):
            insights.update({criteria.slug: criterias_holder[index]})

        # create forcasted list
        forecasted_list = forecasted_df.apply(
            lambda row: {"year": row.name, "metrics": row.to_dict()}, axis=1
        ).tolist()

        final_model = Assessment(
            symbol=symbol,
            forecast=forecasted_list,
            insights=insights,
            updated_at=datetime.now(),
        )
        # save the record
        assessmentRepo.save(final_model)
        print_pink_bold(f"=== Inserted assessment for {symbol}")


if __name__ == "__main__" or __name__ == "tasks":
    main()
