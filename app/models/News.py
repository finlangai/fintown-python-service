from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

import math
from typing import Optional, Dict, Any
from bson import ObjectId

from core.mongodb import get_database
from datetime import datetime


class News(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    symbol: Optional[str]
    title: Optional[str]
    price: Optional[float]
    price_change: Optional[float]
    price_change_ratio: Optional[float]
    price_change_ratio_1m: Optional[float]
    publish_date: Optional[datetime]

    class Config:
        populate_by_name = True


class NewsRepository(AbstractRepository[News]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "news"
