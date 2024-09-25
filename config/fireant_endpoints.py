# === FIREANT API ENDPOINTS

# placeholder: symbol
ENDPOINT_FUNDAMENTAL = "https://restv2.fireant.vn/symbols/{}/fundamental"

# placeholder: symbol, params: type(1,2,3,4), year: int, quarter(1,2,3,4), limit: int
ENDPOINT_FINANCIAL_STATEMENT = (
    "https://restv2.fireant.vn/symbols/{}/full-financial-reports"
)

# placeholder: symbol | params: count: int
# ENDPOINT_DIVIDENDS = "https://restv2.fireant.vn/symbols/{}/dividends"

# placeholder: symbol, limit | params: count: int
ENDPOINT_DIVIDENDS = "https://restv2.fireant.vn/events/search"

# placeholder: symbol
ENDPOINT_HOLDERS = "https://restv2.fireant.vn/symbols/{}/holders"

# placeholder: symbol
ENDPOINT_PROFILE = "https://restv2.fireant.vn/symbols/{}/profile"
