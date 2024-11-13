from app.enums import FormulaType


def get():
    return {
        "identifier": "discounted-cash-flow",
        "name": "Mô hình chiết khấu dòng tiền (Discounted Cash Flow - DCF)",
        "formular": "{free_cash_flow} / (1 + {r}) ** {t}",
        "params": {},
        "metadata": {"category": FormulaType.STOCK_VALUATION},
    }
