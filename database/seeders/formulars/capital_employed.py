from app.models import Expression, Formular
from app.enums import FormulaType

from database.seeders.formulars.parameters import CurrentLiabilities, TotalAsset

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{TotalAsset.slug}}} - {{{CurrentLiabilities.slug}}}",
    parameters=[TotalAsset, CurrentLiabilities],
)


def get(order: int):
    return Formular(
        category=FormulaType.FINANCIAL_METRIC,
        name="Capital Employed",
        name_vi="Vốn được sử dụng",
        abbr="CE",
        identifier="capital_employed",
        order=order,
        description="Capital Employed (Vốn Được Sử Dụng) là chỉ số đo lường tổng số vốn mà công ty đã đầu tư vào hoạt động kinh doanh để tạo ra lợi nhuận. Chỉ số này bao gồm vốn chủ sở hữu và nợ dài hạn, cho thấy tổng nguồn lực tài chính mà công ty sử dụng để duy trì và mở rộng hoạt động của mình.",
        library=[BASIC],
    )
