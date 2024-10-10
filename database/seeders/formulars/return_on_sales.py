from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import OperatingProfitLoss, NetSales

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{OperatingProfitLoss.slug}}} / {{{NetSales.slug}}} * 100",
    parameters=[OperatingProfitLoss, NetSales],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=True,
        unit=None,
    )
    return Formular(
        category=FormulaType.FINANCIAL_METRIC,
        name="Return on Sales",
        name_vi="Tỷ suất lợi nhuận trên doanh thu",
        display_name="ROS",
        identifier="return_on_sales",
        description="ROS (Return on Sales), hay Tỷ Suất Lợi Nhuận Trên Doanh Thu, là chỉ số đo lường khả năng sinh lời của công ty từ doanh thu thuần. Chỉ số này cho biết mỗi đồng doanh thu tạo ra bao nhiêu đồng lợi nhuận, phản ánh hiệu quả hoạt động kinh doanh và khả năng kiểm soát chi phí.",
        metadata=meta,
        library=[BASIC],
    )
