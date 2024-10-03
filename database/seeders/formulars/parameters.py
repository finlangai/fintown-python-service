from app.models import Parameter, ParamLocation

# ===== BALANCE SHEET
TotalAsset = Parameter(
    field="TOTAL ASSETS (Bn. VND)",
    slug="total_assets_bn_vnd",
    location=ParamLocation.balance_sheet,
)

OwnerEquity = Parameter(
    field="OWNER'S EQUITY(Bn.VND)",
    slug="owner_s_equity_bn_vnd",
    location=ParamLocation.balance_sheet,
)

Liabilities = Parameter(
    field="LIABILITIES (Bn. VND)",
    slug="liabilities_bn_vnd",
    location=ParamLocation.balance_sheet,
)

CurrentAsset = Parameter(
    field="CURRENT ASSETS (Bn. VND)",
    slug="current_assets_bn_vnd",
    location=ParamLocation.balance_sheet,
)

CurrentLiabilities = Parameter(
    field="Current liabilities (Bn. VND)",
    slug="current_liabilities_bn_vnd",
    location=ParamLocation.balance_sheet,
)

NetInventories = Parameter(
    field="Net Inventories",
    slug="net_inventories",
    location=ParamLocation.balance_sheet,
)

CashAndCashEquivalents = Parameter(
    field="Cash and cash equivalents (Bn. VND)",
    slug="cash_and_cash_equivalents_bn_vnd",
    location=ParamLocation.balance_sheet,
)

ShortTermBorrowings = Parameter(
    field="Short-term borrowings (Bn. VND)",
    slug="short_term_borrowings_bn_vnd",
    location=ParamLocation.balance_sheet,
)

LongTermBorrowings = Parameter(
    field="Long-term borrowings (Bn. VND)",
    slug="long_term_borrowings_bn_vnd",
    location=ParamLocation.balance_sheet,
)

# ===== INCOME STATEMENT
Sales = Parameter(
    field="Sales",
    slug="sales",
    location=ParamLocation.income_statement,
)

NetSales = Parameter(
    field="Net Sales",
    slug="net_sales",
    location=ParamLocation.income_statement,
)

NetProfit = Parameter(
    field="Net Profit For the Year",
    slug="net_profit_for_the_year",
    location=ParamLocation.income_statement,
)

TotalOperatingRevenue = Parameter(
    field="Total operating revenue",
    slug="total_operating_revenue",
    location=ParamLocation.income_statement,
)

GrossProfit = Parameter(
    field="Gross Profit",
    slug="gross_profit",
    location=ParamLocation.income_statement,
)

CostOfSales = Parameter(
    field="Cost of Sales",
    slug="cost_of_sales",
    location=ParamLocation.income_statement,
    is_allow_negative=False,
)

AttributableToParentCompany = Parameter(
    field="Attributable to parent company",
    slug="attributable_to_parent_company",
    location=ParamLocation.income_statement,
)

ProfitBeforeTax = Parameter(
    field="Profit before tax",
    slug="profit_before_tax",
    location=ParamLocation.income_statement,
)

SalesDeductions = Parameter(
    field="Sales deductions",
    slug="sales_deductions",
    location=ParamLocation.income_statement,
    is_allow_negative=False,
)

InterestExpenses = Parameter(
    field="Interest Expenses",
    slug="interest_expenses",
    location=ParamLocation.income_statement,
    is_allow_negative=False,
)

# ===== CASHFLOW STATEMENT

# ===== RATIO
OutstandingShare = Parameter(
    field="Outstanding Share (Mil. Shares)",
    slug="outstanding_share_mil_shares",
    location=ParamLocation.ratio,
)

MarketCap = Parameter(
    field="Market Capital (Bn. VND)",
    slug="market_capital_bn_vnd",
    location=ParamLocation.ratio,
)

# ===== MARKET PRICE
ClosedPrice = Parameter(
    field="Closed Price", slug="closed_price", location=ParamLocation.market_price
)
