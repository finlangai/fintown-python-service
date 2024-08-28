from app.models import Expression, Formular, Parameter
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    CurrentAsset,
    CurrentLiabilities,
    NetInventories,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"({{{CurrentAsset.slug}}} - {{{NetInventories.slug}}}) / {{{CurrentLiabilities.slug}}}",
    parameters=[CurrentAsset, CurrentLiabilities, NetInventories],
)


def get(order: int):
    return Formular(
        category=FormulaType.FINANCIAL_METRIC,
        name="Quick Ratio",
        name_vi="Hệ số thanh toán nhanh",
        abbr="QR",
        identifier="quick_ratio",
        order=order,
        description="Quick Ratio (Hệ Số Thanh Toán Nhanh) là chỉ số đo lường khả năng thanh toán ngắn hạn của công ty bằng cách so sánh tài sản lưu động có tính thanh khoản cao với nợ ngắn hạn. Chỉ số này cho biết công ty có thể dùng ngay tài sản lưu động nào để trả các khoản nợ ngắn hạn mà không cần bán hàng tồn kho, phản ánh mức độ an toàn tài chính trong ngắn hạn.",
        library=[BASIC],
    )
