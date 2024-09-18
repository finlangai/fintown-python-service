from core import mongodb as database
from typing import List

from app.enums import StatementType
from app.models import (
    FinancialStatement,
    CompanyRepository,
    FinancialStatementRepository,
)
from app.services import get_financial_statement
from app.utils import text_to_red, print_green_bold

from config.seeder.config import STATEMENT_QUARTERLY_LIMIT, STATEMENT_YEARLY_LIMIT


def main():
    print_green_bold("=== SEEDING FINANCIAL STATEMENTS")
    # MUỐN SEED THỦ CÔNG MÃ NHẤT ĐỊNH THÌ DÙNG FILTER
    companies: List = database.query_with_projection(
        CompanyRepository.Meta.collection_name, {}, {"symbol", "icb_code"}
    )
    StatementRepo = FinancialStatementRepository()

    # === Lấy dữ liệu raw của các loại báo cáo tài chính
    for company in companies:
        # LOGGING THE STARTING POINT OF SEEDING FOR EACH COMPANY
        print(f"== seeding for {text_to_red(company['symbol'].upper())}")

        # === Lặp lại 2 lần để lấy báo cáo tài chính cả theo quý lẫn theo năm
        for timeline in [
            {
                "title": "quarterly",
                "quarter_index": 4,
                "limit": STATEMENT_QUARTERLY_LIMIT,
            },
            {"title": "yearly", "quarter_index": 0, "limit": STATEMENT_YEARLY_LIMIT},
        ]:

            try:
                # Chứa báo cáo tài chính đã xử lý qua các lần lặp
                statement_list: list[FinancialStatement] = []

                # ĐỊNH NGHĨA HÀM CLOSURE
                def get_statement(type: StatementType):
                    return get_financial_statement(
                        symbol=company["symbol"],
                        type=type,
                        limit=timeline["limit"],
                        quarter=timeline["quarter_index"],
                    )

                # Lấy dạng LCTT dựa theo mã ICB
                cashflow_type = FinancialStatement.check_cashflow_type(
                    code=company["icb_code"]
                )

                # LẤY DỮ LIỆU RAW CHO CÁC LOẠI BÁO CÁO
                raw_data_list = [
                    get_statement(type=statement_type)
                    for statement_type in [
                        StatementType.BALANCE_SHEET,
                        StatementType.INCOME_STATEMENT,
                        cashflow_type,
                    ]
                ]

                # KIỂM TRA TRƯỜNG HỢP KHÔNG CÓ DỮ LIỆU LCTT ĐỂ LẤY DẠNG CÒN LẠI
                if raw_data_list[2] is None:
                    # Replace dạng LCTT hiện tại với dạng còn lại
                    cashflow_type = (
                        StatementType.CASHFLOW_INDIRECT
                        if cashflow_type != StatementType.CASHFLOW_INDIRECT
                        else StatementType.CASHFLOW_DIRECT
                    )
                    # Thay thế vị trí thứ 3 trong mảng là cashflow statement với dữ liệu mới
                    raw_data_list[2] = get_statement(type=cashflow_type)

                # Lấy loại số lượng được trả về lớn nhất trong 3 loại làm chuẩn số lần lặp
                timestamps: list = max(
                    [statements[0]["values"] for statements in raw_data_list],
                    key=len,
                )

                is_cf_direct = cashflow_type == StatementType.CASHFLOW_DIRECT
                # LẶP QUA TỪNG MỐC THỜI GIAN
                for stamp in timestamps:
                    statements = [
                        FinancialStatement.statement_formatter(
                            data, stamp.get("period")
                        )
                        for data in raw_data_list
                    ]
                    financial_statement = FinancialStatement(
                        symbol=company["symbol"],
                        year=stamp["year"],
                        quarter=stamp["quarter"],
                        balance_sheet=statements[0],
                        income_statement=statements[1],
                        is_cashflow_direct=is_cf_direct,
                        cashflow_statement=statements[2],
                    )

                    statement_list.append(financial_statement)
                # INSERT CURRENT PROCESSING STATEMENTS
                StatementRepo.save_many(statement_list)
                # LOGGING STATEMENT TIMELINE
                print(f"{len(timestamps)} {timeline['title']} statements inserted")

            except Exception as e:
                e.with_traceback()
                print(f"An error occurred: {e}")

        print(f"Done for {text_to_red(company['symbol'].upper())}")
        print("---------")


if __name__ == "__main__" or __name__ == "tasks":
    main()
