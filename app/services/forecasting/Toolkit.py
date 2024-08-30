import numpy as np


class ForecastingToolkit:
    def __init__(self):
        pass

    def prepare_data(self, data):
        # Convert list of Pydantic models into numpy arrays
        sizes = np.array([[item.size] for item in data])
        prices = np.array([item.price for item in data])
        return sizes, prices
