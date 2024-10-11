from app.models import Expression, Formular, FormularMeta
from app.enums import FormulaType

from database.seeders.formulars.parameters import (
    NetSales,
    TotalAsset,
    Sales,
    SalesDeductions,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{NetSales.slug}}} / {{{TotalAsset.slug}}}",
    parameters=[NetSales, TotalAsset],
)
# === SECONDARY
SECONDARY = Expression(
    name="Secondary",
    expression=f"({{{Sales.slug}}} - {{{SalesDeductions.slug}}}) / {{{TotalAsset.slug}}}",
    parameters=[Sales, SalesDeductions, TotalAsset],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        is_percentage=False,
        order=order,
        unit="vòng",
    )
    return Formular(
        id=order,
        name="Asset Turnover",
        name_vi="Vòng quay tài sản",
        display_name="Vòng quay tài sản",
        identifier="asset_turnover",
        description="Asset Turnover (Vòng Quay Tài Sản) là chỉ số đo lường hiệu quả sử dụng tài sản của công ty để tạo ra doanh thu. Chỉ số này cho biết mỗi đồng tài sản giúp công ty tạo ra bao nhiêu đồng doanh thu, phản ánh khả năng tối ưu hóa tài sản trong việc sản xuất doanh thu.",
        metadata=meta,
        library=[BASIC, SECONDARY],
    )
