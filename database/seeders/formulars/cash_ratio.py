from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    CashAndCashEquivalents,
    CurrentLiabilities,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{CashAndCashEquivalents.slug}}} / {{{CurrentLiabilities.slug}}}",
    parameters=[CashAndCashEquivalents, CurrentLiabilities],
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
        name="Cash Ratio",
        name_vi="Hệ số thanh toán bằng tiền mặt",
        display_name="Hệ số thanh toán bằng tiền mặt",
        identifier="cash_ratio",
        description="Cash Ratio, hay Hệ Số Thanh Toán Bằng Tiền Mặt, là chỉ số đo lường khả năng thanh toán ngắn hạn của công ty bằng cách so sánh lượng tiền mặt và các khoản tương đương tiền với nợ ngắn hạn. Chỉ số này cho biết công ty có bao nhiêu tiền mặt ngay lập tức để trả các khoản nợ ngắn hạn mà không cần thanh lý tài sản khác, phản ánh mức độ an toàn tài chính trong ngắn hạn.",
        metadata=meta,
        library=[BASIC],
    )
