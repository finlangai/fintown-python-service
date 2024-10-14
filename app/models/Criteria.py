from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

from typing import List

from core.mongodb import get_database


class CriteriaCluster(BaseModel):
    name: str
    metrics: List[str]


class Criteria(BaseModel):
    id: int = Field(default=None, alias="_id")
    name: str
    slug: str
    group: List[CriteriaCluster]

    class Config:
        populate_by_name = True


class CriteriaRepository(AbstractRepository[Criteria]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "criterias"
