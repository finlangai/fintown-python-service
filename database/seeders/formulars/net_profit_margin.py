from app.models import Expression, Formular, Parameter
from app.enums import ParamLocation, FormulaType

NetProfit = Parameter(
    field="Net Profit For the Year",
    slug="net_profit_for_the_year",
    location=ParamLocation.income_statement,
)
NetSales = Parameter(
    field="Net Sales",
    slug="net_sales",
    location=ParamLocation.income_statement,
)
TotalOperatingRevenue = Parameter(
    field="Total operating revenue",
    slug="total_operating_revenue",
    location=ParamLocation.income_statement,
)
Sales = Parameter(
    field="Sales",
    slug="sales",
    location=ParamLocation.income_statement,
)
SalesDeductions = Parameter(
    field="Sales deductions",
    slug="sales_deductions",
    location=ParamLocation.income_statement,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"({{ {NetProfit.slug} }} / {{ {NetSales.slug} }}) * 100",
    parameters=[NetProfit, NetSales],
)
# === SECONDARY
SECONDARY = Expression(
    name="Secondary",
    expression=f"({{ {NetProfit.slug} }} / {{ {TotalOperatingRevenue.slug} }}) * 100",
    parameters=[NetProfit, TotalOperatingRevenue],
)
# === TERTIARY
TERTIARY = Expression(
    name="Tertiary",
    expression=f"{{ {NetProfit.slug} }} / ({{ {Sales.slug} }} - {{ {SalesDeductions.slug} }}) * 100",
    parameters=[NetProfit, Sales, SalesDeductions],
)


def get(order: int):
    return Formular(
        category=FormulaType.FINANCIAL_METRIC,
        name="Net Profit Margin",
        name_vi="Biên lợi nhuận ròng",
        identifier="net_profit_margin",
        order=order,
        description="Net Profit Margin (biên lợi nhuận ròng) là tỷ lệ phần trăm lợi nhuận ròng so với doanh thu thuần của công ty. Nó cho biết công ty giữ lại bao nhiêu phần trăm doanh thu sau khi trừ đi tất cả các chi phí, bao gồm chi phí hoạt động, lãi vay và thuế.",
        library=[BASIC, SECONDARY, TERTIARY],
    )
