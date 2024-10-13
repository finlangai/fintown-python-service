from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import GrossProfit, GrossProfitPrevious

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{GrossProfit.slug}}} - {{{GrossProfitPrevious.slug}}} ) / {{{GrossProfitPrevious.slug}}} * 100",
    parameters=[GrossProfit, GrossProfitPrevious],
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
        name="Gross Profit Growth Rate",
        name_vi="Tỷ lệ tăng trưởng lợi nhuận gộp",
        display_name="Tỷ lệ tăng trưởng lợi nhuận gộp",
        identifier="gross_profit_growth_rate",
        description="Gross Profit Growth Rate (Tỷ Lệ Tăng Trưởng Lợi Nhuận Gộp) là chỉ số đo lường mức độ thay đổi của lợi nhuận gộp của công ty trong một khoảng thời gian nhất định. Chỉ số này cho biết lợi nhuận gộp đã tăng hoặc giảm bao nhiêu phần trăm so với kỳ trước, phản ánh khả năng kiểm soát chi phí sản xuất và doanh thu từ hoạt động kinh doanh.",
        metadata=meta,
        library=[BASIC],
    )
