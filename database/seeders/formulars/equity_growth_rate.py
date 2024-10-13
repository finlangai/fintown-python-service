from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import OwnerEquity, OwnerEquityPrevious

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{OwnerEquity.slug}}} - {{{OwnerEquityPrevious.slug}}} ) / {{{OwnerEquityPrevious.slug}}} * 100",
    parameters=[OwnerEquity, OwnerEquityPrevious],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=True,
        unit=None,
        is_viewable=False,
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="Equity Growth Rate",
        name_vi="Tỷ lệ tăng trưởng vốn chủ sỡ hữu",
        display_name="Tăng trưởng vốn chủ sỡ hữu",
        identifier="equity_growth_rate",
        description="Assets Growth Rate (Tỷ Lệ Tăng Trưởng Tài Sản) là chỉ số đo lường mức độ thay đổi của tổng tài sản của công ty trong một khoảng thời gian nhất định. Chỉ số này cho biết tổng tài sản đã tăng hoặc giảm bao nhiêu phần trăm so với kỳ trước, phản ánh sự phát triển và mở rộng của công ty.",
        metadata=meta,
        library=[BASIC],
    )
