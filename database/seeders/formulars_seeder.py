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
    # Change the order of module to change the order
    formulars = [
        gross_profit_margin,
        net_profit_margin,
        earnings_per_share,
        price_to_earnings,
        price_to_book,
        ev_to_ebit,
        return_of_equity,
        return_of_asset,
        return_of_capital_employed,
        quick_ratio,
        asset_turnover,
        capital_employed,
        debt_to_equity,
    ]
    formulars = [
        formular_module.get(index + 1)
        for index, formular_module in enumerate(formulars)
    ]
    for f in formulars:
        print_green_bold(f"=== {f.name}")

    FormularRepository().save_many(models=formulars)


if __name__ == "__main__" or __name__ == "tasks":
    main()
