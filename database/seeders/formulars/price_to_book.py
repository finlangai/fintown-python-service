from app.models import Expression, Formular, FormularMeta
from app.enums import FormulaType

from database.seeders.formulars.parameters import (
    NetSales,
    TotalAsset,
    OwnerEquity,
    OutstandingShare,
    ClosedPrice,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{ClosedPrice.slug}}} / ( {{{OwnerEquity.slug}}} / {{{OutstandingShare.slug}}} )",
    parameters=[ClosedPrice, OwnerEquity, OutstandingShare],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        is_percentage=False,
        order=order,
    )
    return Formular(
        name="Price to Book",
        name_vi="Tỷ lệ giá trên giá trị sổ sách",
        display_name="P/B",
        identifier="price_to_book",
        description="P/B (Price to Book), hay Tỷ Lệ Giá trên Giá Trị Sổ Sách, là chỉ số đo lường mối quan hệ giữa giá thị trường của cổ phiếu và giá trị sổ sách trên mỗi cổ phiếu. Chỉ số này cho biết nhà đầu tư đang trả bao nhiêu cho mỗi đồng giá trị tài sản ròng của công ty, phản ánh mức độ định giá tài sản của công ty so với giá trị thực tế được ghi nhận trên sổ sách kế toán.",
        metadata=meta,
        library=[BASIC],
    )
