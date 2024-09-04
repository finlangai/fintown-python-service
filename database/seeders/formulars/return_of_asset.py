from app.models import Expression, Formular, FormularMeta
from app.enums import FormulaType

from database.seeders.formulars.parameters import (
    AttributableToParentCompany,
    TotalAsset,
    NetProfit,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    # expression=f"({{{AttributableToParentCompany.slug}}} / {{{TotalAsset.slug}}}) * 100",
    expression=f"({{{NetProfit.slug}}} / {{{TotalAsset.slug}}}) * 100",
    parameters=[NetProfit, TotalAsset],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=True,
        unit=None,
    )
    return Formular(
        category=FormulaType.FINANCIAL_METRIC,
        name="Return on Assets",
        name_vi="Tỷ lệ lợi nhuận trên tổng tài sản",
        abbr="ROA",
        identifier="return_on_assets",
        description="ROA (Return on Assets), hay Tỷ Suất Lợi Nhuận Trên Tổng Tài Sản, là chỉ số đo lường khả năng sinh lời của một công ty dựa trên tổng tài sản mà công ty sở hữu. Chỉ số này cho biết lợi nhuận mà công ty tạo ra từ mỗi đồng tài sản, phản ánh hiệu quả sử dụng tài sản để tạo ra lợi nhuận.",
        metadata=meta,
        library=[BASIC],
    )
