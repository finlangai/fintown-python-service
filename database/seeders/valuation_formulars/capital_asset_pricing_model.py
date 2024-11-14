from app.enums import FormulaType


def get():
    return {
        "identifier": "capital-asset-pricing-model",
        "name": "Mô hình CAPM (Capital Asset Pricing Model)",
        "formular": "{risk_free_rate} + {beta} * ( {market_return} - {risk_free_rate} )",
        "params": {"risk_free_rate": 0.029},
        "metadata": {"category": FormulaType.STOCK_VALUATION},
    }
