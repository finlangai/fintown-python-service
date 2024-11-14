from app.enums import FormulaType


def get():
    return {
        "identifier": "price-earnings-to-growth-ratio",
        "name": "Phương pháp định giá cổ phiếu theo hệ số PEG (Price/Earnings to Growth)",
        "formular": "{price_to_earnings} / {earnings_per_share_growth_rate}",
        "params": {},
        "metadata": {"category": FormulaType.STOCK_VALUATION},
    }
