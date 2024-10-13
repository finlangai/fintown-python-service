from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import TotalAsset, TotalAssetPrevious

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{TotalAsset.slug}}} - {{{TotalAssetPrevious.slug}}} ) / {{{TotalAssetPrevious.slug}}} * 100",
    parameters=[TotalAsset, TotalAssetPrevious],
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
        name="Assets Growth Rate",
        name_vi="Tỷ lệ tăng trưởng tài sản",
        display_name="Tỷ lệ tăng trưởng tài sản",
        identifier="assets_growth_rate",
        description="Assets Growth Rate (Tỷ Lệ Tăng Trưởng Tài Sản) là chỉ số đo lường mức độ thay đổi của tổng tài sản của công ty trong một khoảng thời gian nhất định. Chỉ số này cho biết tổng tài sản đã tăng hoặc giảm bao nhiêu phần trăm so với kỳ trước, phản ánh sự phát triển và mở rộng của công ty.",
        metadata=meta,
        library=[BASIC],
    )
