from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

from typing import List, Optional, Dict, Any
from bson import ObjectId

from core.mongodb import get_database


class Forecasted(BaseModel):
    year: Optional[int] = None
    metrics: Optional[Dict[str, Any]] = None


class Assessment(BaseModel):
    """
    This class storing future predictions of metrics and insights about those metrics from LLM
    """

    id: Optional[str] = Field(default=None, alias="_id")
    symbol: Optional[str] = None
    updated_year: Optional[int] = None
    forecasts: Optional[List[Forecasted]] = None
    insights: Optional[Dict[str, Any]] = None

    @field_validator("id", mode="before")
    def set_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class AssessmentRepository(AbstractRepository[Assessment]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "assessments"
