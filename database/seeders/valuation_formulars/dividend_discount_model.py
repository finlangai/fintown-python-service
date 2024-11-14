from app.enums import FormulaType


def get():
    return {
        "identifier": "dividend-discount-model",
        "name": "Mô hình chiết khấu cổ tức (Dividend Discount Model - DDM)",
        "formular": "{D1} / ( {r} - {g} )",
        "params": {"risk_free_rate": 0.029},
        "metadata": {"category": FormulaType.STOCK_VALUATION},
    }
