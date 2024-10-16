from app.models import Expression, Formular, FormularMeta
from app.enums import FormulaType

from database.seeders.formulars.parameters import (
    OutstandingShare,
    TotalAsset,
    Liabilities,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"( {{{TotalAsset.slug}}} - {{{Liabilities.slug}}} ) / {{{OutstandingShare.slug}}}",
    parameters=[TotalAsset, Liabilities, OutstandingShare],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        is_percentage=False,
        order=order,
        is_viewable=False,
    )
    return Formular(
        id=order,
        name="Book Value Per Share",
        name_vi="Giá trị sổ sách trên mỗi cổ phiếu",
        display_name="BVPS",
        identifier="book_value_per_share",
        description="Book Value Per Share (Giá Trị Sổ Sách Trên Mỗi Cổ Phiếu) là chỉ số đo lường giá trị tài sản ròng của công ty trên mỗi cổ phiếu. Chỉ số này cho biết giá trị tài sản còn lại mà mỗi cổ đông sở hữu nếu công ty thanh lý tất cả tài sản và trả hết các khoản nợ.",
        metadata=meta,
        library=[BASIC],
    )
