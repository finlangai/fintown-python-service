from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import OperatingProfitLoss, InterestExpenses

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{OperatingProfitLoss.slug}}} / {{{InterestExpenses.slug}}}",
    parameters=[OperatingProfitLoss, InterestExpenses],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=False,
        unit=None,
        is_viewable=False,
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="Interest Coverage Ratio",
        name_vi="Hệ số bảo toàn lãi vay",
        display_name="Hệ số bảo toàn lãi vay",
        identifier="interest_coverage_ratio",
        description="Interest Coverage Ratio, hay Hệ Số Bảo Toàn Lãi Vay, là chỉ số đo lường khả năng của công ty trong việc chi trả lãi vay từ lợi nhuận hoạt động. Chỉ số này cho biết công ty kiếm được bao nhiêu lợi nhuận trước lãi vay và thuế (EBIT) so với chi phí lãi vay, giúp đánh giá mức độ an toàn trong việc đáp ứng các nghĩa vụ tài chính",
        metadata=meta,
        library=[BASIC],
    )
