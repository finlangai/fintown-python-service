from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import Revenue, RevenuePrevious

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{Revenue.slug}}} - {{{RevenuePrevious.slug}}} ) / {{{RevenuePrevious.slug}}} * 100",
    parameters=[Revenue, RevenuePrevious],
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
        name="Revenue Growth Rate",
        name_vi="Tỷ lệ tăng trưởng doanh thu",
        display_name="Tăng trưởng doanh thu",
        identifier="revenue_growth_rate",
        description="Revenue Growth Rate (Tỷ Lệ Tăng Trưởng Doanh Thu) là chỉ số đo lường mức độ tăng trưởng doanh thu của công ty trong một khoảng thời gian nhất định. Chỉ số này cho biết doanh thu đã tăng hoặc giảm bao nhiêu phần trăm so với kỳ trước, giúp đánh giá sự phát triển của doanh nghiệp qua thời gian.",
        metadata=meta,
        library=[BASIC],
    )
