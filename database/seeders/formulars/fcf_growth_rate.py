from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    FreeCashFlow,
    FreeCashFlowPrevious,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{FreeCashFlow.slug}}} - {{{FreeCashFlowPrevious.slug}}} ) / {{{FreeCashFlowPrevious.slug}}} * 100",
    parameters=[FreeCashFlow, FreeCashFlowPrevious],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=True,
        unit=None,
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="FCF Growth Rate",
        name_vi="Tỷ lệ tăng trưởng dòng tiền tự do",
        display_name="Tăng trưởng FCF",
        identifier="free_cash_flow_growth_rate",
        description="FCF Growth Rate (Tỷ Lệ Tăng Trưởng Dòng Tiền Tự Do) là chỉ số đo lường mức độ thay đổi của dòng tiền tự do (Free Cash Flow - FCF) của công ty qua các kỳ tài chính. Chỉ số này cho biết FCF đã tăng hoặc giảm bao nhiêu phần trăm so với kỳ trước, phản ánh khả năng tạo ra tiền mặt của doanh nghiệp sau khi đã trang trải chi phí vốn.",
        metadata=meta,
        library=[BASIC],
    )
