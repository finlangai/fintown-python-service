from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    OperatingProfitLoss,
    DepreciationAndAmortisation,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{OperatingProfitLoss.slug}}} + {{{DepreciationAndAmortisation.slug}}}",
    parameters=[OperatingProfitLoss, DepreciationAndAmortisation],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=False,
        unit="Tỷ đồng",
        is_should_divine_by_billion=True,
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="Earnings Before Interest, Taxes, Depreciation, and Amortization",
        name_vi="Lợi nhuận trước lãi vay, thuế và khấu hao",
        display_name="EBITDA",
        identifier="ebitda",
        description="EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) là chỉ số tài chính đo lường lợi nhuận của công ty trước khi trừ các khoản lãi vay, thuế, khấu hao và chi phí khấu hao tài sản vô hình. Chỉ số này giúp đánh giá hiệu quả hoạt động kinh doanh thuần túy của doanh nghiệp mà không bị ảnh hưởng bởi các quyết định tài chính và kế toán.",
        metadata=meta,
        library=[BASIC],
    )
