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

    def metrics(self) -> pd.DataFrame:
        metrics_df = pd.DataFrame()

        # calculate EPS LTM
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

        # concat EPS LTM Dataframe
        metrics_df = pd.concat([metrics_df, eps_ltm.to_frame()], axis=1)

        # === calculate regular metrics
        from config.formular_resolver import METRICS_LOCATION_IDENTIFIERS

        formular_identifers = METRICS_LOCATION_IDENTIFIERS
        required_formulars = list(
            FormularRepository().find_by({"identifier": {"$in": formular_identifers}})
        )
        # loop through each formular and concat it to the metrics_df
        for formular in required_formulars:
            metric_series = self.appraise(formular)
            if metric_series is None:
                continue
            metric_series.rename(f"{formular.name}", inplace=True)
            metrics_df = pd.concat([metrics_df, metric_series.to_frame()], axis=1)

        return metrics_df

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
            TotalAsset,
            OwnerEquity,
            CurrentAsset,
            CurrentLiabilities,
        )

        previous_df = pd.DataFrame()

        columns = [
            Revenue,
            NetProfit,
            GrossProfit,
            TotalAsset,
            OwnerEquity,
            CurrentAsset,
            CurrentLiabilities,
        ]

        for param in columns:
            location_df = self.get_data(param.location)
            if param.field in location_df:
                previous_df[param.field] = self.choose_best_column(
                    df=location_df[param.field], name=param.slug
                )

        metrics_df = self.get_data(ParamLocation.metrics)

        previous_df = pd.concat([previous_df, metrics_df], axis=1)

        previous_df.columns = [
            col_name + " Previous" for col_name in previous_df.columns
        ]

        # return the Dataframe while shifting up by one row, which make each row the previous period
        return previous_df.shift(-1)

    def delta(self):
        from database.seeders.formulars.parameters import (
            CurrentAsset,
            CurrentLiabilities,
            OwnerEquity,
        )

        delta_df = pd.DataFrame()

        # === calculate Working Capital Delta
        try:

            current_assets = self.get_column(CurrentAsset)
            current_liabilities = self.get_column(CurrentLiabilities)
            working_capital = current_assets - current_liabilities
            working_capital_delta = working_capital - working_capital.shift(-1)
            working_capital_delta.name = "Working Capital Delta"

            delta_df = pd.concat([delta_df, working_capital_delta.to_frame()], axis=1)
        except:
            pass

        # === calculate Owner Equity Delta
        try:
            owner_equity = self.get_column(OwnerEquity)
            owner_equity_delta = owner_equity - owner_equity.shift(-1)
            owner_equity_delta.name = "Owner Equity Delta"

            delta_df = pd.concat([delta_df, owner_equity_delta.to_frame()], axis=1)
        except:
            pass

        return delta_df
