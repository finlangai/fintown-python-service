from pydantic import BaseModel


class Dividend(BaseModel):
    year: int
    cash_dividend: int
    stock_dividend: int
    total_assets: int
    stock_holder_equity: int
