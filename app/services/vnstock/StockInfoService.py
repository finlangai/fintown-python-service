from pandas import DataFrame
from app.types import SourceType
from app.services.vnstock import BaseVnStockService


class StockInfoService(BaseVnStockService):
    def __init__(self, symbol: str = "VCI", source: SourceType = "TCBS"):
        super().__init__(symbol, source)
        self.company = self.stock.company

    def overview(self) -> DataFrame:
        return self.company.overview()

    def profile(self) -> DataFrame:
        return self.company.profile()

    def subsidiaries(self) -> DataFrame:
        return self.company.subsidiaries()

    def events(self) -> DataFrame:
        return self.company.events()

    def news(self) -> DataFrame:
        return self.company.news()
