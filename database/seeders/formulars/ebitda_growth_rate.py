from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import EBITDA, EBITDAPrevious

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{EBITDA.slug}}} - {{{EBITDAPrevious.slug}}} ) / {{{EBITDAPrevious.slug}}} * 100",
    parameters=[EBITDA, EBITDAPrevious],
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
        name="EBITDA Growth Rate",
        name_vi="Tỷ lệ tăng trưởng lợi nhuận trước thuế, lãi vay và khấu hao",
        display_name="Tăng trưởng EBITDA",
        identifier="ebitda_growth_rate",
        description="EBITDA Growth Rate (Tỷ Lệ Tăng Trưởng EBITDA) là chỉ số đo lường mức độ thay đổi của EBITDA của công ty trong một khoảng thời gian nhất định. Chỉ số này cho biết EBITDA đã tăng hoặc giảm bao nhiêu phần trăm so với kỳ trước, phản ánh khả năng sinh lời và hiệu quả hoạt động kinh doanh của doanh nghiệp.",
        metadata=meta,
        library=[BASIC],
    )
