from app.models import Formula, Expression, Parameter
from app.enums import ParamLocation, FormulaType


GrossProfit = Parameter(
    field="Gross Profit",
    slug="gross_profit",
    location=ParamLocation.INCOME_STATEMENT,
)
NetSales = Parameter(
    field="Net Sales",
    slug="net_sales",
    location=ParamLocation.INCOME_STATEMENT,
)
Sales = Parameter(
    field="Sales",
    slug="sales",
    location=ParamLocation.INCOME_STATEMENT,
)
SalesDeductions = Parameter(
    field="Sales deductions",
    slug="sales_deductions",
    location=ParamLocation.INCOME_STATEMENT,
    is_allow_zero=True,
    is_allow_negative=False,
)
CostOfSales = Parameter(
    field="Cost of Sales",
    slug="cost_of_sales",
    location=ParamLocation.INCOME_STATEMENT,
    is_allow_zero=True,
    is_allow_negative=False,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"({GrossProfit.slug} / {NetSales.slug}) * 100",
    parameters=[GrossProfit, NetSales],
)

# === USING COGS
USING_COGS = Expression(
    name="Using COGS",
    expression=f"({Sales.slug} - {SalesDeductions.slug} - {CostOfSales.slug}) / ({Sales.slug} - {SalesDeductions.slug}) * 100",
    parameters=[Sales, SalesDeductions, CostOfSales],
)


def get(order: int):
    return Formula(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        name="Gross Profit Margin",
        identifier="gross_profit_margin",
        description="Gross Profit Margin (biên lợi nhuận gộp) là tỷ lệ phần trăm lợi nhuận gộp so với doanh thu thuần của công ty. Nó cho biết công ty giữ lại bao nhiêu phần trăm doanh thu sau khi trừ đi chi phí sản xuất trực tiếp.",
        library=[BASIC, USING_COGS],
    )
