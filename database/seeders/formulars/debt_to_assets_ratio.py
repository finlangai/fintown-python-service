from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    Liabilities,
    TotalAsset,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{Liabilities.slug}}} / {{{TotalAsset.slug}}} * 100",
    parameters=[Liabilities, TotalAsset],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=True,
        unit=None,
        is_viewable=False,
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="Debt to Assets Ratio",
        name_vi="Tỷ lệ nợ trên tài sản",
        display_name="Tỷ lệ nợ trên tài sản",
        identifier="debt_to_assets_ratio",
        description="Debt to Assets Ratio (Tỷ Lệ Nợ Trên Tài Sản) là chỉ số đo lường mức độ tài sản của công ty được tài trợ bởi các khoản nợ phải trả. Chỉ số này cho biết phần trăm tổng tài sản của công ty được chi trả bằng nợ phải trả, bao gồm cả nợ vay và các khoản phải trả khác. Nó phản ánh rủi ro tài chính và khả năng trả nợ của doanh nghiệp.",
        metadata=meta,
        library=[BASIC],
    )
