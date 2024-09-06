from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from ..Toolkit import ForecastingToolkit
import pandas as pd


class LinearRegressionForecaster(ForecastingToolkit):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.model = LinearRegression()
        self.lastest_year = None

    def train(self, X_2d, y_1d):
        """
        Fit the model to the data.

        :param X_2d: 2D array-like of shape (n_samples, n_features)
        :param y_1d: 1D array-like of shape (n_samples,)
        """
        self.model.fit(X_2d, y_1d)

    def forecast(self, initial: pd.Series, years_ahead: int) -> pd.Series:
        """
        Take in the initial series of the metrics and how many years ahead to forecast iteratively with Linear Regression
        """
        # get the lastest year
        lastest_year: int = initial.index.max()

        # loop through the
        for count in range(years_ahead):
            # reset the model
            self.reset()

            years_2d = initial.index.values.reshape(-1, 1)
            targets_1d = initial.values

            self.train(X_2d=years_2d, y_1d=targets_1d)
            target_year = lastest_year + count + 1
            predicted_value = self.model.predict(X=[[target_year]])[0]
            initial.loc[target_year] = predicted_value

        # return forecasted portion of the series, which is from the latest year in the initial + 1
        return initial.loc[lastest_year + 1 :]
