from app.models import AssessmentCluster, CriteriaCluster, AssessmentCriteria, Criteria
from config.llm.prompts import (
    thesis_input_template,
    criteria_thesis_prompt,
    metric_input_template,
    cluster_review_prompt,
    overall_input_template,
    overall_prompt,
)

import pandas as pd


class PromptHelper:
    @staticmethod
    def craft_cluster(
        symbol: str,
        cluster: CriteriaCluster,
        metrics_df: pd.DataFrame,
        forecasted_df: pd.DataFrame,
        formulars_dict: dict,
    ):
        metrics_data = ""
        # map the metrics data for prompting
        for identifier in cluster.metrics:
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

        # create prompt for cluster assessment
        prompt_for_cluster = cluster_review_prompt.format(
            metrics_data=metrics_data,
            metric_cluster_name=cluster.name,
            symbol=symbol,
        )
        return prompt_for_cluster

    @staticmethod
    def craft_criteria(
        symbol: str,
        clusters_holder: list[AssessmentCluster],
        criteria_name: str,
        group: list[CriteriaCluster],
    ):
        thesis_input = ""
        # loop through each cluster to generate thesis_input
        for index, cluster in enumerate(clusters_holder):
            if cluster is None:
                continue
            thesis_input += thesis_input_template.format(
                cluster_name=group[index].name,
                status=cluster.status,
                review=cluster.assessment,
            )
        # create prompt for criteria thesis
        criteria_prompt = criteria_thesis_prompt.format(
            criteria_name=criteria_name,
            symbol=symbol,
            thesis_input=thesis_input,
        )
        return criteria_prompt

    @staticmethod
    def craft_overall(
        symbol: str,
        criterias_holder: list[AssessmentCriteria],
        criterias_list: list[Criteria],
    ):
        overall_input = ""
        for index, criteria in enumerate(criterias_holder):
            overall_input += overall_input_template.format(
                criteria_name=criterias_list[index].name,
                status=criteria.status,
                assessment=criteria.assessment,
            )
        # create prompt for overall assessment
        overall_assessment_prompt = overall_prompt.format(
            symbol=symbol, overall_input=overall_input
        )
        return overall_assessment_prompt
