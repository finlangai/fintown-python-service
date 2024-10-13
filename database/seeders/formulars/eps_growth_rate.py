from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    EarningsPerShareLTM,
    EarningsPerShareLTMPrevious,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{EarningsPerShareLTM.slug}}} - {{{EarningsPerShareLTMPrevious.slug}}} ) / {{{EarningsPerShareLTMPrevious.slug}}} * 100",
    parameters=[EarningsPerShareLTM, EarningsPerShareLTMPrevious],
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
        name="EPS Growth Rate",
        name_vi="Tỷ lệ tăng trưởng lợi nhuận trên cổ phiếu",
        display_name="Tăng trưởng EPS",
        identifier="earnings_per_share_growth_rate",
        description="EPS Growth Rate (Tỷ Lệ Tăng Trưởng Lợi Nhuận Trên Cổ Phiếu) là chỉ số đo lường mức độ thay đổi của lợi nhuận trên mỗi cổ phiếu (EPS) của công ty qua các kỳ tài chính. Chỉ số này cho biết EPS đã tăng hoặc giảm bao nhiêu phần trăm so với kỳ trước, giúp đánh giá khả năng sinh lời của công ty cho mỗi cổ phiếu trong quá trình phát triển.",
        metadata=meta,
        library=[BASIC],
    )
