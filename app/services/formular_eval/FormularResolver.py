from app.services.formular_eval import ResolverToolkit
from app.models import Formular
import pandas as pd


class FormularResolver(ResolverToolkit):
    def appraise(self, metric: Formular) -> pd.DataFrame | None:
        # Loop through each formular
        for formular in metric.library:
            # Chech if having enough parameters to calculate with the current formular
            is_sufficient = self.check_sufficiency(parameters=formular.parameters)
            if not is_sufficient:
                continue

            # Loop through and accumulate required parameters in a single dataframe
            required_df = pd.DataFrame()
            for param in formular.parameters:
                column = self.get_column(param=param)
                required_df = pd.concat([required_df, column], axis=1)

            result: pd.Series = required_df.apply(
                lambda row: self.safe_eval(formular.expression.format(**row)), axis=1
            )

            # change the name of the series into its metric identifier
            result.name = metric.identifier

            # stop the loop since the formular is capable of calculating
            break

        # If any formular capable of calculating the metric, return the result, if not, left None
        return locals().get("result", None)
