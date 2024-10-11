from app.models import Expression, Formular, FormularMeta
from app.enums import FormulaType

from database.seeders.formulars.parameters import (
    NetProfit,
    OutstandingShare,
    ClosedPrice,
    EarningsPerShareLTM,
)

# === BASIC
# BASIC = Expression(
#     name="Basic",
#     expression=f"{{{ClosedPrice.slug}}} / ( {{{NetProfit.slug}}} / {{{OutstandingShare.slug}}} )",
#     parameters=[ClosedPrice, NetProfit, OutstandingShare],
# )
BASIC = Expression(
    name="Basic",
    expression=f"{{{ClosedPrice.slug}}} / {{{EarningsPerShareLTM.slug}}}",
    parameters=[ClosedPrice, EarningsPerShareLTM],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        is_percentage=False,
        order=order,
    )
    return Formular(
        id=order,
        name="Price to Earnings",
        name_vi="Tỷ lệ giá trên lợi nhuận",
        display_name="P/E",
        identifier="price_to_earnings",
        description="P/E (Price to Earnings), hay Tỷ Lệ Giá trên Lợi Nhuận, là chỉ số đo lường mối quan hệ giữa giá thị trường của cổ phiếu và lợi nhuận trên mỗi cổ phiếu (EPS). Chỉ số này cho biết nhà đầu tư đang trả bao nhiêu cho mỗi đồng lợi nhuận mà công ty tạo ra, phản ánh mức độ định giá của cổ phiếu và kỳ vọng tăng trưởng lợi nhuận trong tương lai.",
        metadata=meta,
        library=[BASIC],
    )
