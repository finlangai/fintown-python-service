from app.services.formular_eval import ResolverToolkit
from app.models import Formular, FormularRepository
from app.enums import ParamLocation
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

    def last_twelve_months(self) -> pd.DataFrame:
        eps_formular = FormularRepository().find_one_by(
            {"identifier": "earnings_per_share"}
        )

        eps_df = self.appraise(eps_formular)
        # reverse the order to calculate
        eps_df = eps_df.iloc[::-1]

        eps_ltm = eps_df.rolling(window=4, min_periods=1).sum()

        # reverse into the right order
        eps_ltm = eps_ltm.iloc[::-1]
        eps_ltm.name = "EPS LTM"

        return eps_ltm.to_frame()

    def average(self) -> pd.DataFrame:
        average_df = pd.DataFrame()

        balance_df = self.get_data(ParamLocation.balance_sheet)
        if "Inventories, Net (Bn. VND)" in balance_df:
            inventories = balance_df["Inventories, Net (Bn. VND)"]

            # reverse to calculate with rolling sum
            inventories = inventories.iloc[::-1]

            # calculate rolling sum and then divide by the window size to get the average
            avg_inventories = inventories.rolling(window=2, min_periods=1).sum() / 2

            # reverse back to the right order
            avg_inventories = avg_inventories.iloc[::-1]

            # handle the last row separately
            avg_inventories.iloc[-1] = inventories.iloc[0]

            # Set Average Inventories column
            average_df["Average Inventories"] = avg_inventories
        return average_df

    def previous(self):
        from database.seeders.formulars.parameters import (
            Revenue,
            NetProfit,
            GrossProfit,
        )

        previous_df = pd.DataFrame()

        income_df = self.get_data(ParamLocation.income_statement)
        income_columns = [Revenue, NetProfit, GrossProfit]

        for param in income_columns:
            if param.field in income_df:
                previous_df[param.field + " Previous"] = self.choose_best_column(
                    df=income_df[param.field], name=param.slug
                )

        # return the Dataframe while shifting up by one row, which make each row the previous period
        return previous_df.shift(-1)
