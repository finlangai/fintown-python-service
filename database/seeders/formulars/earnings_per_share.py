from app.models import Expression, Formular, FormularMeta
from app.enums import FormulaType

from database.seeders.formulars.parameters import (
    AttributableToParentCompany,
    OutstandingShare,
    NetProfit,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    # expression=f"{{{AttributableToParentCompany.slug}}} / {{{OutstandingShare.slug}}}",
    expression=f"{{{NetProfit.slug}}} / {{{OutstandingShare.slug}}}",
    parameters=[OutstandingShare, NetProfit],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        is_percentage=False,
        order=order,
        unit="VNĐ/CP",
    )
    return Formular(
        category=FormulaType.FINANCIAL_METRIC,
        name="Earnings Per Share",
        name_vi="Lợi nhuận trên mỗi cổ phiếu",
        abbr="EPS",
        identifier="earnings_per_share",
        description="EPS (Earnings Per Share), hay Lợi Nhuận trên Mỗi Cổ Phiếu, là chỉ số đo lường phần lợi nhuận ròng của công ty thuộc về mỗi cổ phiếu đang lưu hành. Chỉ số này cho biết số tiền lợi nhuận mà mỗi cổ đông nhận được cho mỗi cổ phiếu của mình, phản ánh khả năng sinh lời của công ty từ góc độ cổ đông.",
        metadata=meta,
        library=[BASIC],
    )
