from app.models import Expression, Formular, FormularMeta
from app.enums import FormulaType

from database.seeders.formulars.parameters import (
    AttributableToParentCompany,
    OwnerEquity,
    NetProfit,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    # expression=f"({{{AttributableToParentCompany.slug}}} / {{{OwnerEquity.slug}}}) * 100",
    expression=f"({{{NetProfit.slug}}} / {{{OwnerEquity.slug}}}) * 100",
    parameters=[NetProfit, OwnerEquity],
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
        name="Return on Equity",
        name_vi="Tỷ lệ lợi nhuận trên vốn chủ sở hữu",
        display_name="ROE",
        identifier="return_on_equity",
        description="ROE (Return on Equity), hay Tỷ Suất Lợi Nhuận Trên Vốn Chủ Sở Hữu, là chỉ số đo lường khả năng sinh lời của một công ty dựa trên vốn chủ sở hữu. Chỉ số này cho biết lợi nhuận mà công ty tạo ra từ mỗi đồng vốn mà cổ đông đầu tư, phản ánh hiệu quả sử dụng vốn của công ty để tạo ra giá trị cho cổ đông.",
        metadata=meta,
        library=[BASIC],
    )
