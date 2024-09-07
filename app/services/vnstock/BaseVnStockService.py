from vnstock3 import Vnstock
from app.types import SourceType
from pandas import DataFrame


class BaseVnStockService:
    def __init__(self, symbol: str = "VCI", source: SourceType = "TCBS"):
        self.stock = Vnstock().stock(symbol=symbol, source=source)
        self.symbol = symbol

    def first_row_to_dict(self, df: DataFrame) -> dict:
        """
        Turn the first row of a dataframe into a dict
        """
        return df.loc[0].to_dict()
