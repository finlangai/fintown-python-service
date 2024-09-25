from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

import math
from typing import Optional, Dict, Any
from bson import ObjectId

from core.mongodb import get_database
from datetime import datetime


class Subsidiary(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    symbol: str
    sub_company_name: str
    sub_own_percent: float

    class Config:
        populate_by_name = True


class SubsidiaryRepository(AbstractRepository[Subsidiary]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "subsidiaries"
