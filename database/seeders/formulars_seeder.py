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
    price_to_book,
    price_to_earnings,
)
from app.models import FormularRepository, Formular
from app.utils import print_green_bold


def main():
    # the number that got passed to get function is the order
    formulars = [
        gross_profit_margin.get(1),
        net_profit_margin.get(2),
        earnings_per_share.get(3),
        price_to_earnings.get(4),
        price_to_book.get(5),
        ev_to_ebit.get(6),
        return_of_equity.get(7),
        return_of_asset.get(8),
        return_of_capital_employed.get(9),
        quick_ratio.get(10),
        asset_turnover.get(11),
        capital_employed.get(12),
        debt_to_equity.get(13),
    ]
    for f in formulars:
        print_green_bold(f"=== {f.name}")

    FormularRepository().save_many(models=formulars)


if __name__ == "__main__" or __name__ == "tasks":
    main()
