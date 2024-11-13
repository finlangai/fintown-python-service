from app.enums import FormulaType


def get():
    return {
        "identifier": "graham-intrinsic-value-formula",
        "name": "Công thức định giá cổ phiếu của Benjamin Graham",
        "formular": "( {earnings_per_share} * (8.5 + 2 * {g}) * 4.4 ) / {Y}",
        "params": {"Y": 3.257},
        "metadata": {"category": FormulaType.STOCK_VALUATION},
    }
