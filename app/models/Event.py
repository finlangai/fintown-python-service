from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

import math
from typing import Optional, Dict, Any
from bson import ObjectId

from core.mongodb import get_database
from datetime import datetime


class Event(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    symbol: Optional[str]
    price: Optional[float]
    price_change: Optional[float]
    price_change_ratio: Optional[float]
    # price_change_ratio_1m: Optional[float]
    event_name: Optional[str]
    event_code: Optional[str]
    event_desc: Optional[str]
    notify_date: Optional[datetime]
    exer_date: Optional[datetime]
    reg_final_date: Optional[datetime]
    exer_right_date: Optional[datetime]

    class Config:
        populate_by_name = True


class EventRepository(AbstractRepository[Event]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "events"
