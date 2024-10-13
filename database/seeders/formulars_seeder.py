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
    current_ratio,
    inventory_turnover,
    return_on_sales,
    weighted_average_cost_of_capital,
    cash_ratio,
    free_cash_flow,
    interest_coverage_ratio,
    debt_to_assets_ratio,
)
from app.models import FormularRepository, Formular
from app.utils import print_green_bold


def main():
    # Change the order of module to change the order
    formulars = [
        free_cash_flow,
        capital_employed,
        debt_to_equity,
        earnings_per_share,
        price_to_earnings,
        price_to_book,
        gross_profit_margin,
        net_profit_margin,
        ev_to_ebit,
        weighted_average_cost_of_capital,
        return_of_equity,
        return_of_asset,
        return_on_sales,
        return_of_capital_employed,
        current_ratio,
        quick_ratio,
        cash_ratio,
        interest_coverage_ratio,
        debt_to_assets_ratio,
        asset_turnover,
        inventory_turnover,
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
