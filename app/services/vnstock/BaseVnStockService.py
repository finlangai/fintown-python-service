from vnstock3 import Vnstock
from app.types import SourceType


class BaseVnStockService:
    def __init__(self, symbol: str = "VCI", source: SourceType = "TCBS"):
        self.stock = Vnstock().stock(symbol=symbol, source=source)
        self.symbol = symbol
