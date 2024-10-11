from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import TotalAsset, Liabilities

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{TotalAsset.slug}}} / {{{Liabilities.slug}}}",
    parameters=[TotalAsset, Liabilities],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=False,
        unit=None,
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="Current Ratio",
        name_vi="Hệ số thanh toán hiện hành",
        display_name="Hệ số thanh toán hiện hành",
        identifier="current_ratio",
        description="Current Ratio, hay Hệ Số Thanh Toán Hiện Hành, là chỉ số đo lường khả năng thanh toán ngắn hạn của công ty bằng cách so sánh tài sản ngắn hạn với nợ ngắn hạn. Chỉ số này cho biết công ty có đủ tài sản lưu động để trả các khoản nợ ngắn hạn khi đến hạn hay không, phản ánh mức độ an toàn tài chính trong ngắn hạn.",
        metadata=meta,
        library=[BASIC],
    )
