from app.models import Expression, Formular, Parameter, FormularMeta
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
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=True,
        unit=None,
    )
    return Formular(
        category=FormulaType.FINANCIAL_METRIC,
        name="Gross Profit Margin",
        name_vi="Biên lợi nhuận gộp",
        display_name="GPM",
        identifier="gross_profit_margin",
        description="GPM (Gross Profit Margin), hay Biên Lợi Nhuận Gộp, là chỉ số đo lường phần trăm doanh thu còn lại sau khi đã trừ đi giá vốn hàng bán. Chỉ số này phản ánh hiệu quả kiểm soát chi phí sản xuất và khả năng sinh lời từ hoạt động kinh doanh chính của công ty.",
        metadata=meta,
        library=[BASIC, USING_COGS],
    )
