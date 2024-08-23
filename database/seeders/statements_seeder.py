from core import mongodb as database
from typing import List

from app.enums import StatementType
from app.models import FinancialStatement, Company
from app.services import get_financial_statement
from app.utils import text_to_red, print_green_bold

from config.config import STATEMENT_QUARTERLY_LIMIT, STATEMENT_YEARLY_LIMIT


def main():
    print_green_bold("=== SEEDING FINANCIAL STATEMENTS")
    # MUỐN SEED THỦ CÔNG MÃ NHẤT ĐỊNH THÌ DÙNG FILTER
    companies: List = database.query_with_projection(
        Company.get_collection_name(), {}, {"_id", "icb_code"}
    )

    # === Lấy dữ liệu raw của các loại báo cáo tài chính
    for company in companies:
        # LOGGING THE STARTING POINT OF SEEDING FOR EACH COMPANY
        print(f"== seeding for {text_to_red(company['_id'].upper())}")

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
                # ĐỊNH NGHĨA HÀM CLOSURE
                def get_statement(type: StatementType):
                    return get_financial_statement(
                        symbol=company["_id"],
                        type=type,
                        limit=timeline["limit"],
                        quarter=timeline["quarter_index"],
                    )

                # LẤY DỮ LIỆU RAW CHO CÁC LOẠI BÁO CÁO
                raw_data_list = [
                    get_statement(type=statement_type)
                    for statement_type in [
                        StatementType.BALANCE_SHEET,
                        StatementType.INCOME_STATEMENT,
                        FinancialStatement.check_cashflow_type(
                            code=company["icb_code"]
                        ),
                    ]
                ]

                # KIỂM TRA TRƯỜNG HỢP KHÔNG CÓ DỮ LIỆU LCTT ĐỂ LẤY DẠNG CÒN LẠI
                if raw_data_list[2] is None:
                    # Lấy type lctt ban đầu
                    cf_type = FinancialStatement.check_cashflow_type(
                        code=company["icb_code"]
                    )
                    # Replace với dạng còn lại
                    cf_type = (
                        StatementType.CASHFLOW_INDIRECT
                        if cf_type != StatementType.CASHFLOW_INDIRECT
                        else StatementType.CASHFLOW_DIRECT
                    )
                    raw_data_list[2] = get_statement(type=cf_type)

                # Lấy loại số lượng được trả về lớn nhất trong 3 loại làm chuẩn số lần lặp
                timestamps: list = max(
                    [statements[0]["values"] for statements in raw_data_list],
                    key=len,
                )

                # HASHMAP ĐỂ MAP TÊN FIELD THÀNH SNAKE CASE
                key_maps = [
                    FinancialStatement.keys_mapper(raw_statement)
                    for raw_statement in raw_data_list
                ]

                # LẶP QUA TỪNG MỐC THỜI GIAN
                for stamp in timestamps:
                    statements = [
                        FinancialStatement.statement_formatter(
                            data, stamp.get("period"), map
                        )
                        for data, map in zip(raw_data_list, key_maps)
                    ]
                    financial_statement = FinancialStatement(
                        symbol=company["_id"],
                        year=stamp["year"],
                        quarter=stamp["quarter"],
                        balance_sheet=statements[0],
                        income_statement=statements[1],
                        cashflow_statement=statements[2],
                    ).__dict__

                    FinancialStatement.insert_parent(doc=financial_statement)
                # LOGGING STATEMENT TIMELINE
                print(f"{len(timestamps)} {timeline['title']} statements inserted")

            except Exception as e:
                # Handle any exception
                e.with_traceback()
                print(f"An error occurred: {e}")

        print(f"Done for {text_to_red(company['_id'].upper())}")
        print("---------")


if __name__ == "__main__":
    main()
