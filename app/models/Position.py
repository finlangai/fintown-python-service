from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

from typing import Optional
import re

from core.mongodb import get_database
from datetime import datetime


class Position(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    name: str

    class Config:
        populate_by_name = True


class PositionRepository(AbstractRepository[Position]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "positions"
