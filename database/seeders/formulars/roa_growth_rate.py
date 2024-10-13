from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    ReturnOnAssets,
    ReturnOnAssetsPrevious,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{ReturnOnAssets.slug}}} - {{{ReturnOnAssetsPrevious.slug}}} ) / {{{ReturnOnAssetsPrevious.slug}}} * 100",
    parameters=[ReturnOnAssets, ReturnOnAssetsPrevious],
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
        name="FCF Growth Rate",
        name_vi="Tăng trưởng tỷ lệ lợi nhuận trên tài sản",
        display_name="Tăng trưởng ROA",
        identifier="return_of_assets_growth_rate",
        description="ROA Growth Rate (Tỷ Lệ Tăng Trưởng Lợi Nhuận Trên Tài Sản) là chỉ số đo lường mức độ thay đổi của ROA (Return on Assets) của công ty trong một khoảng thời gian. Chỉ số này cho biết ROA đã tăng hoặc giảm bao nhiêu phần trăm so với kỳ trước, phản ánh sự cải thiện hoặc suy giảm trong việc sử dụng tài sản để tạo ra lợi nhuận.",
        metadata=meta,
        library=[BASIC],
    )
