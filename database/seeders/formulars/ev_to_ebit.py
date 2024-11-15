from app.models import Expression, Formular, FormularMeta
from app.enums import FormulaType

from database.seeders.formulars.parameters import (
    MarketCap,
    CashAndCashEquivalents,
    ShortTermBorrowings,
    LongTermBorrowings,
    ProfitBeforeTax,
    OperatingProfitLoss,
    Liabilities,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    # expression=f"({{{MarketCap.slug}}} + {{{ShortTermBorrowings.slug}}} + {{{LongTermBorrowings.slug}}} - {{{CashAndCashEquivalents.slug}}}) / ({{{ProfitBeforeTax.slug}}} + {{{InterestExpenses.slug}}})",
    # expression=f"({{{MarketCap.slug}}} + {{{ShortTermBorrowings.slug}}} + {{{LongTermBorrowings.slug}}} - {{{CashAndCashEquivalents.slug}}}) / {{{OperatingProfitLoss.slug}}}",
    expression=f"({{{MarketCap.slug}}} + {{{Liabilities.slug}}} - {{{CashAndCashEquivalents.slug}}}) / {{{OperatingProfitLoss.slug}}}",
    parameters=[
        MarketCap,
        Liabilities,
        CashAndCashEquivalents,
        OperatingProfitLoss,
    ],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=False,
        unit=None,
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="Enterprise Value to Earnings Before Interest and Taxes",
        name_vi="Tỷ lệ giá trị doanh nghiệp trên lợi nhuận trước lãi vay và thuế",
        display_name="EV/EBIT",
        identifier="enterprise_value_to_earnings_before_interest_and_taxes",
        description="EV/EBIT (Enterprise Value to Earnings Before Interest and Taxes), hay Tỷ Lệ Giá Trị Doanh Nghiệp trên Lợi Nhuận Trước Lãi Vay và Thuế, là chỉ số đo lường giá trị doanh nghiệp so với lợi nhuận trước lãi vay và thuế. Chỉ số này cho biết mỗi đồng lợi nhuận trước lãi vay và thuế tương ứng với bao nhiêu đồng giá trị doanh nghiệp, phản ánh mức độ định giá của công ty và khả năng tạo ra lợi nhuận từ hoạt động kinh doanh.",
        metadata=meta,
        library=[BASIC],
    )
