from core import mongodb
import numpy as np, pandas as pd, json
from datetime import timedelta


from app.utils import (
    print_green_bold,
    model_mapper,
    json_camel_to_snake,
    text_to_red,
    time,
)
from app.models import CompanyRepository, FormularRepository
from app.services import StockQuoteService, FormularResolver
from app.enums import ParamLocation
from .formulars.parameters import (
    ShortTermBorrowings,
    LongTermBorrowings,
    InterestExpenses,
    TaxForTheYear,
    Liabilities,
    ProfitBeforeTax,
)


def main():
    """ """
    print_green_bold("=== SEEDING WACC VALUE FOR STASH")
    # get the list of symbol from companies symbol
    symbols = mongodb.query_with_projection(
        CompanyRepository.Meta.collection_name, {}, {"_id": 0, "symbol": 1}
    )
    symbol_list = [record["symbol"] for record in symbols]

    resolver = FormularResolver(dropna=True, period="year")

    # === GET FORMULARS
    wacc_info = mongodb.find_one(
        "formular_library", {"identifier": "weighted_average_cost_of_capital"}
    )
    capm_info = mongodb.find_one(
        "formular_library", {"identifier": "capital-asset-pricing-model"}
    )
    wacc_formular: str = wacc_info["library"][0]["expression"]
    capm_formular: str = capm_info["formular"]

    # === GET PARAMS
    market_return = mongodb.find_one("stash", {"symbol": "VN-INDEX"})["market_return"]

    # cho risk free rate bằng với tỷ suất trái phiếu 15 năm chính phủ Việt Nam, tạm thời code cứng
    risk_free_rate = 0.029

    # get the list of beta value and turn it into a dict for easier look up when calculating
    raw_beta_list = mongodb.query_with_projection(
        "stash", {"is_stock": {"$ne": False}}, {"_id": 0, "symbol": 1, "beta": 1}
    )
    # beta dict
    beta_dict = {record["symbol"]: record["beta"] for record in list(raw_beta_list)}

    # for symbol in symbol_list:
    for symbol in symbol_list:
        print_green_bold(f"=== {symbol}")
        resolver.update_symbol(symbol)
        try:

            # Re, calcula using CAPM formular
            capm_expression = capm_formular.format(
                risk_free_rate=risk_free_rate,
                beta=beta_dict[symbol],
                market_return=market_return,
            )
            Re = eval(capm_expression)
            print(f"Re: ", Re)

            # == GET PARAMS FOR WACC FROM FINANCIAL REPORT
            ratio_df = resolver.get_data(ParamLocation.ratio)
            # balance_df = resolver.get_data(ParamLocation.balance_sheet)
            market_cap = int(ratio_df.iloc[0]["Market Capital (Bn. VND)"])
            print("V (market_cap): ", market_cap)

            # interest expenses for calculating Rd
            try:
                interest_expenses = int(resolver.get_column(InterestExpenses).iloc[0])
            except:
                try:
                    # using Interest and Similar Expenses as alternative if normal interest expenses is not present
                    interest_expenses = abs(
                        int(
                            resolver.get_data(ParamLocation.income_statement)[
                                "Interest and Similar Expenses"
                            ].iloc[0]
                        )
                    )
                except:
                    interest_expenses = 0

            # market value of debt or D
            try:
                short_term_borrowing = int(
                    resolver.get_column(ShortTermBorrowings).iloc[0]
                )
                long_term_borrowing = int(
                    resolver.get_column(LongTermBorrowings).iloc[0]
                )
                market_value_of_debt = short_term_borrowing + long_term_borrowing
            except:
                try:
                    # use Placements with and loans to other credit institutions as alternative if not present, for bank
                    market_value_of_debt = int(
                        resolver.get_data(ParamLocation.balance_sheet)[
                            "Placements with and loans to other credit institutions"
                        ].iloc[0]
                    )
                except:
                    # use only short term borrowing if none of the above present, this is for stock company
                    market_value_of_debt = short_term_borrowing

            print("D (market_value_of_debt): ", market_value_of_debt)
            print("Rd: ", interest_expenses / market_value_of_debt)

            # tax column is a bit complicated so
            try:
                tax_for_the_year = int(resolver.get_column(TaxForTheYear).iloc[0])
            except:
                tax_current = resolver.get_data(ParamLocation.income_statement)[
                    "Business income tax - current"
                ].iloc[0]
                tax_deferred = resolver.get_data(ParamLocation.income_statement)[
                    "Business income tax - deferred"
                ].iloc[0]
                tax_for_the_year = abs(int(tax_current + tax_deferred))

            # calculate total tax
            profit_before_tax = int(resolver.get_column(ProfitBeforeTax).iloc[0])

            # print("tax_for_the_year: ", tax_for_the_year)
            # print("profit_before_tax: ", profit_before_tax)
            print(f"Tc: ", tax_for_the_year / profit_before_tax)

            wacc_expression = wacc_formular.format(
                market_capital_bn_vnd=market_cap,
                market_value_of_debt=market_value_of_debt,
                interest_expenses=interest_expenses,
                tax_for_the_year=tax_for_the_year,
                profit_before_tax=profit_before_tax,
                cost_of_equity=Re,
            )
            wacc = eval(wacc_expression)
            print(f"wacc của {text_to_red(symbol)}: ", wacc)

            mongodb.update_one("stash", {"symbol": symbol}, {"wacc": wacc})
            print_green_bold(f"WACC updated for {symbol}")

        except:
            print(f"Có lỗi xảy ra khi tính toán WACC cho {symbol}")


if __name__ == "__main__" or __name__ == "tasks":
    main()
