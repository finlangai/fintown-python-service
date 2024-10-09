from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

import math
from typing import Optional, Dict, Any
from bson import ObjectId

from core.mongodb import get_database
from datetime import datetime


class Transaction(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    symbol: Optional[str]
    transaction_man: Optional[str]
    transaction_man_position: Optional[str]

    related_man_position: Optional[str]
    related_man: Optional[str]

    volume_before_transaction: Optional[int]
    volume_after_transaction: Optional[int]

    plan_buy_volume: Optional[int]
    plan_sell_volume: Optional[int]

    real_sell_volume: Optional[int]
    real_end_date: Optional[int]

    transaction_note: Optional[str]
    ownership: Optional[float]

    plan_begin_date: Optional[int]
    plan_end_date: Optional[int]
    real_buy_volume: Optional[int]
    published_date: Optional[int]
    order_date: Optional[int]

    class Config:
        populate_by_name = True


class TransactionRepository(AbstractRepository[Transaction]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "internal_transactions"
