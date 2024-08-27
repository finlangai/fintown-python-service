from enum import Enum


class ParamLocation(int, Enum):
    """
    Value must be of StockFinanceService's methods
    """

    ratio = 0
    balance_sheet = 1
    income_statement = 2
    cash_flow = 3
