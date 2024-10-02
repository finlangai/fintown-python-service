from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

import math
from typing import Optional, Dict, Any
from bson import ObjectId

from core.mongodb import get_database
from datetime import datetime


class StockQuote(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    symbol: str
    time: int
    interval: int
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[float]

    class Config:
        populate_by_name = True


class StockQuoteRepository(AbstractRepository[StockQuote]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "stock_quotes"
