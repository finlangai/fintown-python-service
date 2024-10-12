from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    MarketCap,
    ShortTermBorrowings,
    LongTermBorrowings,
    InterestExpenses,
    TaxForTheYear,
    ProfitBeforeTax,
    EarningsPerShareLTM,
    ClosedPrice,
)

# === BASIC
# Market ket value of equity
E = f"{{{MarketCap.slug}}}"
# Market value of Debt, or Total Debt
D = f"( {{{ShortTermBorrowings.slug}}} + {{{LongTermBorrowings.slug}}} )"
# V = E + D
V = f"( {E} + {D} )"
# Cost of Debt
Rd = f"( {{{InterestExpenses.slug}}} / {D} )"
# Corporate tax
Tc = f"( {{{TaxForTheYear.slug}}} / {{{ProfitBeforeTax.slug}}} * 100 )"
# Cost of equity, using Earnings Capitalization Ratio or Earnings Yield for alternative
Re = f"( {{{EarningsPerShareLTM.slug}}} / {{{ClosedPrice.slug}}} )"

basic_first_part = f"( {E} / ( {E} + {D} ) ) +  {Re}"
basic_second_part = f"( {D} / ( {E} + {D} ) ) * {Rd}"
basic_third_part = f"( 1 - {Tc} )"

BASIC = Expression(
    name="Basic",
    expression=f"{basic_first_part} + {basic_second_part} * {basic_third_part}",
    parameters=[
        MarketCap,
        ShortTermBorrowings,
        LongTermBorrowings,
        InterestExpenses,
        TaxForTheYear,
        ProfitBeforeTax,
        EarningsPerShareLTM,
        ClosedPrice,
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
        name="Weighted Average Cost of Capital",
        name_vi="Chi Phí Vốn Bình Quân Gia Quyền",
        display_name="WACC",
        identifier="weighted_average_cost_of_capital",
        description="WACC (Weighted Average Cost of Capital), hay Chi Phí Vốn Bình Quân Gia Quyền, là chỉ số đo lường chi phí trung bình mà một công ty phải trả để sử dụng cả vốn vay và vốn chủ sở hữu. WACC thể hiện mức sinh lời tối thiểu mà công ty cần đạt được để bù đắp cho chi phí sử dụng vốn, phản ánh mức độ rủi ro của các khoản đầu tư.",
        metadata=meta,
        library=[BASIC],
    )
