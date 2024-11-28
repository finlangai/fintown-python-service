from enum import Enum


class ParamLocation(int, Enum):
    """
    Value must be of StockFinanceService's methods
    """

    # In StockFinanceService
    ratio = 0
    balance_sheet = 1
    income_statement = 2
    cash_flow = 3
    market_price = 4
    # In FormularResolver
    metrics = 5
    average = 6
    previous = 7
    delta = 8
