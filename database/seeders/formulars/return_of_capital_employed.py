from app.models import Expression, Formular, FormularMeta
from app.enums import FormulaType

from database.seeders.formulars.parameters import (
    ProfitBeforeTax,
    InterestExpenses,
    TotalAsset,
    CurrentLiabilities,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"(({{{ProfitBeforeTax.slug}}} + {{{InterestExpenses.slug}}}) / ({{{TotalAsset.slug}}} - {{{CurrentLiabilities.slug}}})) * 100",
    parameters=[
        ProfitBeforeTax,
        InterestExpenses,
        TotalAsset,
        CurrentLiabilities,
    ],
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
        name="Return on Capital Employed",
        name_vi="Tỷ suất lợi nhuận trên vốn được sử dụng",
        display_name="ROCE",
        identifier="return_on_capital_employed",
        description="Return on Capital Employed (ROCE), hay Tỷ Suất Lợi Nhuận Trên Vốn Được Sử Dụng, là chỉ số đo lường hiệu quả sử dụng vốn trong việc tạo ra lợi nhuận. Chỉ số này cho biết mỗi đồng vốn được sử dụng để đầu tư vào công ty tạo ra bao nhiêu đồng lợi nhuận trước lãi vay và thuế, phản ánh khả năng sinh lời và hiệu quả của việc sử dụng vốn trong hoạt động kinh doanh.",
        metadata=meta,
        library=[BASIC],
    )
