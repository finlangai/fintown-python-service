from pydantic import BaseModel
from core import mongodb as db

from config import CASHFLOW_DIRECT_ICB_CODES, CF_DIRECT_ICB_BLACKLIST
from typing import Optional
from app.enums import StatementType


class FinancialStatement(BaseModel):
    symbol: str
    year: int
    quarter: int
    balance_sheet: Optional[object] = None
    income_statement: Optional[object] = None
    cashflow_statement: Optional[object] = None

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
    def statement_formatter(data: list, period: str, keys_map: dict[str:str]):
        """
        data: mảng dữ liệu gốc khi get báo cáo tài chính
        period: thời điểm của dữ liệu của báo cáo cụ thể trong mảng values ở từng field

        Nhận vào mảng dữ liệu cùng period của quý hoặc năm
        của báo cáo cần lấy sau đó trả về báo cáo đó dưới dạng object
        """

        # Kiểm tra thời điểm có tồn tại trong báo cáo tài chính được trả về hay không
        is_present = next(
            (
                timestamp
                for timestamp in data[0]["values"]
                if timestamp.get("period") == period
            ),
            None,
        )
        if is_present is None:
            return None

        statement = {
            keys_map[field["name"]]: next(
                (
                    metric["value"]
                    for metric in field["values"]
                    if metric.get("period") == period
                )
            )
            for field in data
        }

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
