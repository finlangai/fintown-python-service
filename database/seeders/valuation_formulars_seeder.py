from core import mongodb
from app.utils import print_green_bold
from database.seeders.valuation_formulars import (
    price_to_earnings_valuation,
    price_to_book_valuation,
    discounted_cash_flow,
    graham_intrinsic_value_formula,
    price_earnings_to_growth_ratio,
)


def main():
    print_green_bold("=== SEEDING VALUATION FORMULARS")

    # valuation_formulars = [price_to_earnings_valuation, price_to_book_valuation]
    valuation_formulars = [price_earnings_to_growth_ratio]

    valuation_formulars = [formular.get() for formular in valuation_formulars]

    mongodb.insert_many("formular_library", valuation_formulars)

    print_green_bold(f"INSERTED {len(valuation_formulars)} VALUATION FORMULARS")


if __name__ == "__main__" or __name__ == "tasks":
    main()
