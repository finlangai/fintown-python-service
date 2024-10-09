from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

from typing import Optional
import re

from core.mongodb import get_database
from datetime import datetime


class Officer(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    name: str
    symbol: str
    is_foreigner: bool
    avatar: str
    position_id: int

    class Config:
        populate_by_name = True


class OfficerRepository(AbstractRepository[Officer]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "officers"
