from core import mongodb
from database.seeders.criterias import (
    profitability,
    solvency,
    revenue_profit,
    cashflow,
    assets_equity,
)
from app.models import CriteriaRepository
from app.utils import print_green_bold


def main():
    # Change the order of module to change the order
    criterias_list = [profitability, solvency, revenue_profit, cashflow, assets_equity]
    criterias_list = [
        criteria_module.get(index + 1)
        for index, criteria_module in enumerate(criterias_list)
    ]
    for c in criterias_list:
        print_green_bold(f"=== {c.name}")

    CriteriaRepository().save_many(models=criterias_list)


if __name__ == "__main__" or __name__ == "tasks":
    main()
