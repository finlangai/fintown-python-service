from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

from typing import Optional
import re

from core.mongodb import get_database
from datetime import datetime


class Dividend(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    symbol: str
    title: str
    type: int
    year: Optional[float] = None
    cash: Optional[float]
    percentage: Optional[float]
    record_date: Optional[datetime]
    registration_date: Optional[datetime]
    execution_date: Optional[datetime]

    class Config:
        populate_by_name = True

    @staticmethod
    def parse_title(title: str) -> dict:
        result = {"percentage": None, "cash": None, "year": None}

        # Pattern for percentage (d:d or d,d)
        percentage_pattern = r"(\d+):(\d+,\d+|\d+)"
        percentage_match = re.search(percentage_pattern, title)
        if percentage_match:
            denominator, numerator = percentage_match.groups()
            # Replace comma with dot for float conversion
            denominator = float(denominator.replace(",", "."))
            numerator = float(numerator.replace(",", "."))
            result["percentage"] = numerator / denominator

        # # Pattern for cash (number followed by đ)
        # cash_pattern = r"(\d+)đ"
        # cash_match = re.search(cash_pattern, title)
        # if cash_match:
        #     result["cash"] = float(cash_match.group(1))

        # Pattern for cash (integer or float followed by đ)
        cash_pattern = r"(\d+(?:[.,]\d+)?)đ"
        cash_match = re.search(cash_pattern, title)
        if cash_match:
            cash_value = cash_match.group(1)
            # Replace comma with dot for float conversion
            cash_value = float(cash_value.replace(",", "."))
            result["cash"] = cash_value

        # Pattern for year (đợt X/YYYY or năm YYYY)
        year_pattern = r"(?:đợt \d+/(\d{4})|năm (\d{4}))"
        year_match = re.search(year_pattern, title)
        if year_match:
            # Match group 1 or group 2 depending on the pattern
            result["year"] = int(year_match.group(1) or year_match.group(2))

        return result


class DividendRepository(AbstractRepository[Dividend]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "dividends"

    def get_by_symbol(self, symbol: str):
        return list(self.find_by(query={"symbol": symbol}))
