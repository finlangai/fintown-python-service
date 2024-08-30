from app.models import Expression, Formular, Parameter
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import Liabilities, OwnerEquity

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"({{{Liabilities.slug}}} / {{{OwnerEquity.slug}}}) * 100",
    parameters=[Liabilities, OwnerEquity],
)


def get(order: int):
    return Formular(
        category=FormulaType.FINANCIAL_METRIC,
        name="Debt to Equity",
        name_vi="Tỷ lệ nợ trên vốn chủ sở hữu",
        abbr="D/E",
        identifier="debt_to_equity",
        order=order,
        description="Debt to Equity (D/E), hay Tỷ Lệ Nợ Trên Vốn Chủ Sở Hữu, là chỉ số đo lường mức độ công ty sử dụng nợ để tài trợ cho tài sản so với vốn chủ sở hữu. Chỉ số này cho biết mỗi đồng vốn chủ sở hữu được hỗ trợ bởi bao nhiêu đồng nợ, phản ánh mức độ rủi ro tài chính và khả năng tự chủ tài chính của công ty.",
        library=[BASIC],
    )