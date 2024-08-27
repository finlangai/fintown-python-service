from app.services.formular_eval import ResolverToolkit
from app.models import Formular
import pandas as pd


class FormularResolver(ResolverToolkit):
    def appraise(self, metric: Formular) -> pd.DataFrame | None:
        for formular in metric.library:
            is_sufficient = self.check_sufficiency(parameters=formular.parameters)
            if not is_sufficient:
                continue

            required_df = pd.DataFrame()
            for param in formular.parameters:
                column = self.get_column(param=param)
                required_df = pd.concat([required_df, column], axis=1)

            result: pd.Series = required_df.apply(
                lambda row: self.safe_eval(formular.expression.format(**row)), axis=1
            )

            result.name = metric.identifier
            # stop the loop since the formular is capable of calculating
            break
        return locals().get("result", None)
