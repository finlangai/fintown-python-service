from pydantic import BaseModel, Field, field_validator, root_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime

from core.mongodb import get_database


class AssessmentCluster(BaseModel):
    assessment: str
    status: str
    # this should be the string of the identifier
    metrics: List[int | str]


class AssessmentCriteria(BaseModel):
    assessment: str
    status: str
    # group of metrics cluster
    groups: List[AssessmentCluster | None]


# class AssessmentInsights(BaseModel):
#     overall: str
#     profitability: AssessmentCriteria
#     solvency: AssessmentCriteria
#     revenue_profit: AssessmentCriteria
#     cashflow: AssessmentCriteria
#     assets_equity: AssessmentCriteria


class AssessmentForecasted(BaseModel):
    year: Optional[int] = None
    metrics: Optional[Dict[str, Any]] = None


class Assessment(BaseModel):
    """
    This class storing future predictions of metrics and insights about those metrics from LLM
    """

    id: Optional[str] = Field(default=None, alias="_id")
    symbol: str
    # assessment from llm
    insights: Dict[str, str | AssessmentCriteria]
    # forecast next five year
    forecast: List[AssessmentForecasted]
    # growth percentage for each metrics
    future_deltas: Dict[str, float]
    # updated time
    updated_at: Optional[datetime] = None

    @field_validator("id", mode="before")
    def set_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    @field_validator("updated_at", mode="before")
    def set_updated_at(cls, v):
        return v or datetime.now(tz="utc")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class AssessmentRepository(AbstractRepository[Assessment]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "assessments"
