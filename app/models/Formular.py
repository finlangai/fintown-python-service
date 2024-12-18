from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

from typing import List, Optional
from bson import ObjectId

from app.enums import FormulaType
from core.mongodb import get_database
from .Expression import Expression


class FormularMeta(BaseModel):
    order: int
    category: FormulaType
    # group: Optional[int] = None
    is_percentage: bool = False
    is_should_divine_by_billion: bool = False
    is_viewable: bool = True
    is_enable: bool = True
    unit: Optional[str] = None


class Formular(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    name: str
    name_vi: str
    display_name: str
    identifier: str
    description: str
    metadata: FormularMeta
    library: list[Expression]

    @field_validator("id", mode="before")
    def set_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class FormularRepository(AbstractRepository[Formular]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "formular_library"

    def get_dict(self, identifiers: list[str]):
        formular_dict = self.find_by({"identifier": {"$in": identifiers}})
        formular_dict = {
            formular.identifier: formular for formular in list(formular_dict)
        }
        return formular_dict
