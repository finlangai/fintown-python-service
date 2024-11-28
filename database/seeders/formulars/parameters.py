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

LongTermLiabilities = Parameter(
    field="Long-term liabilities (Bn. VND)",
    slug="long_term_liabilities_bn_vnd",
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
Revenue = Parameter(
    field="Revenue (Bn. VND)",
    slug="revenue_bn_vnd",
    location=ParamLocation.income_statement,
)

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

OperatingProfitLoss = Parameter(
    field="Operating Profit/Loss",
    slug="operating_profit_loss",
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

TaxForTheYear = Parameter(
    field="Tax For the Year",
    slug="tax_for_the_year",
    location=ParamLocation.income_statement,
    is_allow_negative=False,
)


# Tiền thu được từ hoạt động mua bán ngoại hối và vàng
NetGainLossFromForeignCurrencyAndGoldDealings = Parameter(
    field="Net gain (loss) from foreign currency and gold dealings",
    slug="net_gain_loss_from_foreign_currency_and_gold_dealings",
    location=ParamLocation.income_statement,
)
# Tiền thu được từ hoạt động đầu tư
NetGainLossFromDisposalOfInvestmentSecurities = Parameter(
    field="Net gain (loss) from disposal of investment securities",
    slug="net_gain_loss_from_disposal_of_investment_securities",
    location=ParamLocation.income_statement,
)
# Lãi lỗ thuần từ hoạt động khác
NetOtherIncomeExpenses = Parameter(
    field="Net Other income/expenses",
    slug="net_other_income_expenses",
    location=ParamLocation.income_statement,
)


# ===== CASHFLOW STATEMENT
DepreciationAndAmortisation = Parameter(
    field="Depreciation and Amortisation",
    slug="depreciation_and_amortisation",
    location=ParamLocation.cash_flow,
)

PurchaseOfFixedAssets = Parameter(
    field="Purchase of fixed assets",
    slug="purchase_of_fixed_assets",
    location=ParamLocation.cash_flow,
    is_allow_negative=False,
)
NetCashFlowFromOperatingActivities = Parameter(
    field="Net cash inflows/outflows from operating activities",
    slug="net_cash_inflows_outflows_from_operating_activities",
    location=ParamLocation.cash_flow,
)

ProceedsFromBorrowings = Parameter(
    field="Proceeds from borrowings",
    slug="proceeds_from_borrowings",
    location=ParamLocation.cash_flow,
)

RepaymentOfBorrowings = Parameter(
    field="Repayment of borrowings",
    slug="repayment_of_borrowings",
    location=ParamLocation.cash_flow,
    is_allow_negative=False,
)

DividendsPaid = Parameter(
    field="Dividends paid",
    slug="dividends_paid",
    is_allow_negative=False,
    location=ParamLocation.cash_flow,
)

# Tiền thu từ thanh lý hoặc nhượng bán tài sản cố định
ProceedsFromDisposalOfFixedAssets = Parameter(
    field="Proceeds from disposal of fixed assets",
    slug="proceeds_from_disposal_of_fixed_assets",
    location=ParamLocation.cash_flow,
)


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

# ===== METRICS
EarningsPerShareLTM = Parameter(
    field="EPS LTM", slug="eps_ltm", location=ParamLocation.metrics
)
EBITDA = Parameter(
    field="Earnings Before Interest, Taxes, Depreciation, and Amortization",
    slug="earnings_before_interest_taxes_depreciation_and_amortization",
    location=ParamLocation.metrics,
)

FreeCashFlow = Parameter(
    field="Free Cash Flow",
    slug="free_cash_flow",
    location=ParamLocation.metrics,
)

ReturnOnAssets = Parameter(
    field="Return on Assets",
    slug="return_on_assets",
    location=ParamLocation.metrics,
)


# ===== Average
AverageInventory = Parameter(
    field="Average Inventories",
    slug="average_inventories",
    location=ParamLocation.average,
)

# ===== Previous
RevenuePrevious = Parameter(
    field="Revenue (Bn. VND) Previous",
    slug="revenue_bn_vnd_previous",
    location=ParamLocation.previous,
)

NetProfitPrevious = Parameter(
    field="Net Profit For the Year Previous",
    slug="net_profit_for_the_year_previous",
    location=ParamLocation.previous,
)

GrossProfitPrevious = Parameter(
    field="Gross Profit Previous",
    slug="gross_profit_previous",
    location=ParamLocation.previous,
)

TotalAssetPrevious = Parameter(
    field="TOTAL ASSETS (Bn. VND) Previous",
    slug="total_assets_bn_vnd_previous",
    location=ParamLocation.previous,
)

CurrentAssetPrevious = Parameter(
    field="CURRENT ASSETS (Bn. VND) Previous",
    slug="current_assets_bn_vnd_previous",
    location=ParamLocation.balance_sheet,
)

CurrentLiabilitiesPrevious = Parameter(
    field="Current liabilities (Bn. VND) Previous",
    slug="current_liabilities_bn_vnd_previous",
    location=ParamLocation.balance_sheet,
)

OwnerEquityPrevious = Parameter(
    field="OWNER'S EQUITY(Bn.VND) Previous",
    slug="owner_s_equity_bn_vnd_previous",
    location=ParamLocation.previous,
)
EarningsPerShareLTMPrevious = Parameter(
    field="EPS LTM Previous", slug="eps_ltm_previous", location=ParamLocation.previous
)

EBITDAPrevious = Parameter(
    field="Earnings Before Interest, Taxes, Depreciation, and Amortization Previous",
    slug="earnings_before_interest_taxes_depreciation_and_amortization_previous",
    location=ParamLocation.previous,
)

FreeCashFlowPrevious = Parameter(
    field="Free Cash Flow Previous",
    slug="free_cash_flow_previous",
    location=ParamLocation.previous,
)

ReturnOnAssetsPrevious = Parameter(
    field="Return on Assets Previous",
    slug="return_on_assets_previous",
    location=ParamLocation.previous,
)

# === DELTA
# Thay đổi vốn lưu động
WorkingCapitalDelta = Parameter(
    field="Working Capital Delta",
    slug="working_capital_delta",
    location=ParamLocation.delta,
)
# Thay đổi vốn chủ sỡ hữu
OwnerEquityDelta = Parameter(
    field="Owner Equity Delta",
    slug="owner_equity_delta",
    location=ParamLocation.delta,
)
