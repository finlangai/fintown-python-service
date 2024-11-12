from app.enums import FormulaType


def get():
    return {
        "identifier": "price_to_book_valuation",
        "name": "Mô hình định giá theo hệ số P/B (Price to Book)",
        "formular": "{book_value_per_share} * {price_to_book}",
        "params": [],
        "metadata": {"category": FormulaType.STOCK_VALUATION},
    }
