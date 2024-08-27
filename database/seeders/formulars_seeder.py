from core import mongodb
from database.seeders.formulars import gross_profit_margin, net_profit_margin
from app.models import FormulaRepository, Formular


def main():
    formulars = [
        gross_profit_margin.get(order=1),
        net_profit_margin.get(order=2),
    ]

    FormulaRepository().save_many(models=formulars)


if __name__ == "__main__" or __name__ == "tasks":
    main()
