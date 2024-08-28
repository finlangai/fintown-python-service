from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

import math
from typing import Optional, Dict, Any
from bson import ObjectId

from core.mongodb import get_database


class MetricHistory(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    symbol: str
    year: int
    quarter: int = 0
    metrics: Dict[str, Any]

    @field_validator("id", mode="before")
    def set_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    @field_validator("metrics", mode="before")
    def remove_none_and_nan_values(cls, metrics):
        return {
            k: v
            for k, v in metrics.items()
            if v is not None and not isinstance(v, float) or not math.isnan(v)
        }

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class MetricHistoryRepository(AbstractRepository[MetricHistory]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "metric_records"
