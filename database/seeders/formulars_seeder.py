from core import mongodb
from database.seeders.formulars import (
    asset_turnover,
    capital_employed,
    debt_to_equity,
    earnings_per_share,
    ev_to_ebit,
    gross_profit_margin,
    net_profit_margin,
    quick_ratio,
    return_of_asset,
    return_of_capital_employed,
    return_of_equity,
)
from app.models import FormularRepository, Formular
from app.utils import print_green_bold


def main():
    formulars = [
        gross_profit_margin.get(1),
        net_profit_margin.get(2),
        earnings_per_share.get(3),
        ev_to_ebit.get(4),
        return_of_equity.get(5),
        return_of_asset.get(6),
        return_of_capital_employed.get(7),
        quick_ratio.get(8),
        asset_turnover.get(9),
        capital_employed.get(10),
        debt_to_equity.get(11),
    ]
    for f in formulars:
        print_green_bold(f"=== {f.name}")

    FormularRepository().save_many(models=formulars)


if __name__ == "__main__" or __name__ == "tasks":
    main()
