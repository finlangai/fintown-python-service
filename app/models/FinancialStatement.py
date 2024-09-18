from pydantic import BaseModel, Field, field_validator
from core import mongodb as db
from pydantic_mongo import AbstractRepository
from pymongo.database import Database
from core.mongodb import get_database

from bson import ObjectId

from config import CASHFLOW_DIRECT_ICB_CODES, CF_DIRECT_ICB_BLACKLIST
from typing import Optional
from app.enums import StatementType


class FinancialStatement(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    symbol: str
    year: int
    quarter: int
    balance_sheet: Optional[list] = None
    income_statement: Optional[list] = None
    is_cashflow_direct: bool
    cashflow_statement: Optional[list] = None

    @field_validator("id", mode="before")
    def set_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

    @staticmethod
    def get_collection_name():
        return "financial_statements"

    @staticmethod
    def insert_parent(doc: dict[str:any]):
        db.insert_one(
            collection_name=FinancialStatement.get_collection_name(), document=doc
        )

    @staticmethod
    def keys_mapper(data: list):
        """
        data: mảng dữ liệu gốc khi get báo cáo tài chính

        Nhận vào mảng dữ liệu gốc và trả về keys map của field
        e.g. {natural_text: snake_case_text}
        """
        map = dict()
        from utils.natural_to_snake import natural_to_snake

        for field in data:
            map[field["name"]] = natural_to_snake(field["name"])

        return map

    @staticmethod
    def statement_formatter(data: list, period: str) -> list | None:
        """
        data: mảng dữ liệu gốc khi get báo cáo tài chính
        period: thời điểm của dữ liệu của báo cáo cụ thể trong mảng values ở từng field

        Input mảng dữ liệu gốc từ fireant và trả về dữ liệu
        """

        # Kiểm tra thời điểm có tồn tại trong báo cáo tài chính được trả về hay không
        period_index = next(
            (
                i
                for i, timestamp in enumerate(data[0]["values"])
                if timestamp.get("period") == period
            ),
            None,
        )

        # Trả về None nếu báo cáo tại thời điểm yêu cầu không tồn tại
        if period_index is None:
            return None

        statement = [field["values"][period_index]["value"] for field in data]

        return statement

    @staticmethod
    def check_cashflow_type(code: int):
        """
        Hàm lấy kiểm tra mã ICB của công ty và quyết định nên cashflow direct hay indirect
        Chỉ kiểm tra 2 kí tự đầu
        """
        number_str = str(code)
        is_getting_direct = any(
            number_str.startswith(str(code)) for code in CASHFLOW_DIRECT_ICB_CODES
        )
        if code != "" and not None and int(code) in CF_DIRECT_ICB_BLACKLIST:
            is_getting_direct = False
        return (
            StatementType.CASHFLOW_DIRECT
            if is_getting_direct
            else StatementType.CASHFLOW_INDIRECT
        )


class FinancialStatementRepository(AbstractRepository[FinancialStatement]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "financial_statements"
