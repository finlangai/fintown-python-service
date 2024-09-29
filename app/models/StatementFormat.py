from pydantic import BaseModel
from typing import List


class ICBRange(BaseModel):
    start: str
    end: str


class FieldInfo(BaseModel):
    id: int
    name: str
    snake_case: str
    level: int
    parent_id: int
    # expanded: bool


class StatementFormat(BaseModel):
    icb_ranges: List[ICBRange]
    structures: dict

    @staticmethod
    def get_collection_name():
        return "statement_formats"
