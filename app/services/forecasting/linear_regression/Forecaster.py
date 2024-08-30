from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from ..Toolkit import ForecastingToolkit


class LinearRegressionForecaster(ForecastingToolkit):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.model = LinearRegression()

    def train(self, X_2d, y_1d):
        """
        Fit the model to the data.

        :param X_2d: 2D array-like of shape (n_samples, n_features)
        :param y_1d: 1D array-like of shape (n_samples,)
        """
        self.model.fit(X_2d, y_1d)

    def forecast(self, X_2d):
        """
        Make predictions using the fitted model.

        :param X_2d: 2D array-like of shape (n_samples, n_features)
        :return: 1D array of predictions
        """
        return self.model.predict(X_2d)
