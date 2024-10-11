from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import CostOfSales, AverageInventory

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{CostOfSales.slug}}} / {{{AverageInventory.slug}}}",
    parameters=[CostOfSales, AverageInventory],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=False,
        unit="vòng",
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="Inventory Turnover",
        name_vi="Vòng quay hàng tồn kho",
        display_name="Vòng quay hàng tồn kho",
        identifier="inventory_turnover",
        description="Inventory Turnover, hay Vòng Quay Hàng Tồn Kho, là chỉ số đo lường số lần hàng tồn kho được bán và thay thế trong một khoảng thời gian nhất định. Chỉ số này cho biết hiệu quả quản lý hàng tồn kho của công ty, phản ánh khả năng chuyển đổi hàng tồn kho thành doanh thu.",
        metadata=meta,
        library=[BASIC],
    )
