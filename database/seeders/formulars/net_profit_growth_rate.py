from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import NetProfit, NetProfitPrevious

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{NetProfit.slug}}} - {{{NetProfitPrevious.slug}}} ) / {{{NetProfitPrevious.slug}}} * 100",
    parameters=[NetProfit, NetProfitPrevious],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=True,
        unit=None,
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="Net Profit Growth Rate",
        name_vi="Tỷ lệ tăng trưởng lợi nhuận ròng",
        display_name="Tỷ lệ tăng trưởng lợi nhuận ròng",
        identifier="net_profit_growth_rate",
        description="Net Profit Growth Rate (Tỷ Lệ Tăng Trưởng Lợi Nhuận Ròng) là chỉ số đo lường mức độ thay đổi của lợi nhuận ròng của công ty qua các kỳ tài chính. Chỉ số này cho biết lợi nhuận ròng của công ty đã tăng hay giảm bao nhiêu phần trăm so với kỳ trước, giúp đánh giá khả năng sinh lời và hiệu quả hoạt động của doanh nghiệp.",
        metadata=meta,
        library=[BASIC],
    )
