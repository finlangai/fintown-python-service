from app.models import Expression, Formular, Parameter
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    GrossProfit,
    NetSales,
    Sales,
    SalesDeductions,
    CostOfSales,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"({{{GrossProfit.slug}}} / {{{NetSales.slug}}}) * 100",
    parameters=[GrossProfit, NetSales],
)

# === USING COGS
USING_COGS = Expression(
    name="Using COGS",
    expression=f"({{{Sales.slug}}} - {{{SalesDeductions.slug}}} - {{{CostOfSales.slug}}}) / ({{{Sales.slug}}} - {{{SalesDeductions.slug}}}) * 100",
    parameters=[Sales, SalesDeductions, CostOfSales],
)


def get(order: int):
    return Formular(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        name="Gross Profit Margin",
        name_vi="Biên lợi nhuận gộp",
        is_percentage=True,
        abbr="GPM",
        identifier="gross_profit_margin",
        description="GPM (Gross Profit Margin), hay Biên Lợi Nhuận Gộp, là chỉ số đo lường phần trăm doanh thu còn lại sau khi đã trừ đi giá vốn hàng bán. Chỉ số này phản ánh hiệu quả kiểm soát chi phí sản xuất và khả năng sinh lời từ hoạt động kinh doanh chính của công ty.",
        library=[BASIC, USING_COGS],
    )
