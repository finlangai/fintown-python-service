from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    NetProfit,
    NetSales,
    TotalOperatingRevenue,
    Sales,
    SalesDeductions,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"({{{NetProfit.slug}}} / {{{NetSales.slug}}}) * 100",
    parameters=[NetProfit, NetSales],
)
# === SECONDARY
SECONDARY = Expression(
    name="Secondary",
    expression=f"({{{NetProfit.slug}}} / {{{TotalOperatingRevenue.slug}}}) * 100",
    parameters=[NetProfit, TotalOperatingRevenue],
)
# === TERTIARY
TERTIARY = Expression(
    name="Tertiary",
    expression=f"{{{NetProfit.slug}}} / ({{{Sales.slug}}} - {{{SalesDeductions.slug}}}) * 100",
    parameters=[NetProfit, Sales, SalesDeductions],
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
        name="Net Profit Margin",
        name_vi="Biên lợi nhuận ròng",
        display_name="NPM",
        identifier="net_profit_margin",
        description="NPM (Net Profit Margin), hay Biên Lợi Nhuận Ròng, là chỉ số đo lường phần trăm lợi nhuận cuối cùng mà công ty thu được từ doanh thu sau khi đã trừ đi tất cả các chi phí, bao gồm giá vốn hàng bán, chi phí hoạt động, chi phí tài chính và thuế. Chỉ số này cho thấy khả năng sinh lời tổng thể của công ty từ hoạt động kinh doanh và là một thước đo quan trọng để đánh giá hiệu quả tài chính.",
        metadata=meta,
        library=[BASIC, SECONDARY, TERTIARY],
    )
