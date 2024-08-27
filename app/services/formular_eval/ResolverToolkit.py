from pandas import DataFrame

from app.models import Parameter
from app.enums import ParamLocation
from app.services.formular_eval import BaseResolver


class ResolverToolkit(BaseResolver):
    def get_column(df: DataFrame, name: str) -> DataFrame:
        return df[name].T.drop_duplicates().T.iloc[:, 0]

    def check_sufficiency(self, parameters: list[Parameter]) -> bool:
        """
        check if the symbol has sufficient parameters to calculate from a formular
        """
        is_sufficient = all(
            param.field in self.get_data(param.location) for param in parameters
        )
        return is_sufficient

    def apply_constraints(value: any, param: Parameter):
        """
        Apply constraints to value
        """
        value = int(value)
        if not param.is_allow_negative:
            value = abs(value)

        return value
