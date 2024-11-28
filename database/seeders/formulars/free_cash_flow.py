from app.models import Expression, Formular, FormularMeta
from app.enums import ParamLocation, FormulaType

from database.seeders.formulars.parameters import (
    NetProfit,
    DepreciationAndAmortisation,
    PurchaseOfFixedAssets,
    ProceedsFromBorrowings,
    RepaymentOfBorrowings,
    WorkingCapitalDelta,
    OwnerEquity,
    OwnerEquityPrevious,
    ProceedsFromDisposalOfFixedAssets,
    NetGainLossFromForeignCurrencyAndGoldDealings,
    NetGainLossFromDisposalOfInvestmentSecurities,
    NetOtherIncomeExpenses,
    OwnerEquityDelta,
)

# === BASIC
BASIC = Expression(
    name="Basic",
    expression=f"{{{NetProfit.slug}}} - {{{PurchaseOfFixedAssets.slug}}} + {{{DepreciationAndAmortisation.slug}}} - {{{WorkingCapitalDelta.slug}}} + ( {{{ProceedsFromBorrowings.slug}}} - {{{RepaymentOfBorrowings.slug}}} )",
    parameters=[
        NetProfit,
        PurchaseOfFixedAssets,
        DepreciationAndAmortisation,
        WorkingCapitalDelta,
        ProceedsFromBorrowings,
        RepaymentOfBorrowings,
    ],
)

# === FOR BANK
GrowthOfCapital = f"{{{OwnerEquityDelta.slug}}}"
OtherIncome = f"( {{{ProceedsFromDisposalOfFixedAssets.slug}}} + {{{NetGainLossFromForeignCurrencyAndGoldDealings.slug}}} + {{{NetGainLossFromDisposalOfInvestmentSecurities.slug}}} + {{{NetOtherIncomeExpenses.slug}}} )"

FOR_BANK = Expression(
    name="FOR_BANK",
    expression=f"{{{NetProfit.slug}}} - {GrowthOfCapital} + {OtherIncome}",
    parameters=[
        NetProfit,
        OwnerEquityDelta,
        ProceedsFromDisposalOfFixedAssets,
        NetGainLossFromForeignCurrencyAndGoldDealings,
        NetGainLossFromDisposalOfInvestmentSecurities,
        NetOtherIncomeExpenses,
    ],
)


def get(order: int):
    meta = FormularMeta(
        category=FormulaType.FINANCIAL_METRIC,
        order=order,
        is_percentage=False,
        unit="Tỷ đồng",
        is_should_divine_by_billion=True,
        is_viewable=False,
    )
    return Formular(
        id=order,
        category=FormulaType.FINANCIAL_METRIC,
        name="Free Cash Flow",
        name_vi="Dòng tiền tự do",
        display_name="Dòng tiền tự do",
        identifier="free_cash_flow",
        description="Free Cash Flow (FCF), hay Dòng Tiền Tự Do, là chỉ số đo lường lượng tiền mặt còn lại sau khi công ty đã chi trả cho các khoản đầu tư vào tài sản cố định và vốn lưu động cần thiết để duy trì và phát triển hoạt động kinh doanh. Chỉ số này cho biết công ty có bao nhiêu tiền mặt tự do để sử dụng cho các mục đích như trả nợ, chi trả cổ tức, hoặc tái đầu tư.",
        metadata=meta,
        library=[BASIC, FOR_BANK],
    )
