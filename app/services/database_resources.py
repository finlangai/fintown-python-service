from app.models import CriteriaRepository, FormularRepository
from app.enums import FormulaType


class DatabaseResources:
    @staticmethod
    def formulars_dict():

        # get the list of formulars and have it as a dict to query with identifier
        formulars_list = list(
            FormularRepository().find_by(
                query={"metadata.category": FormulaType.FINANCIAL_METRIC}
            )
        )
        formulars_dict = {f.identifier: f for f in formulars_list}
        return formulars_dict

    @staticmethod
    def criterias_list():
        # get the list of criterias
        criterias_list = list(
            CriteriaRepository().find_by(
                query={},
            )
        )
        return criterias_list
