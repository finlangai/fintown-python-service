from app.enums import FormulaType


def get():
    return {
        "identifier": "price_to_earnings_valuation",
        "name": "Mô hình định giá theo hệ số P/E (Price to Earnings)",
        "formular": "{earnings_per_share} * {price_to_earnings}",
        "params": [],
        "metadata": {"category": FormulaType.STOCK_VALUATION},
    }
