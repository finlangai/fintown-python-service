from pydantic import BaseModel, Field
from pydantic_mongo import AbstractRepository
from pymongo.database import Database
from typing import Optional

from core.mongodb import get_database


class Profile(BaseModel):
    head_quarters: Optional[str]
    phone: Optional[str]
    fax: Optional[str]
    email: Optional[str]
    web_address: Optional[str]
    employees: Optional[int]
    business_license_number: Optional[str]
    date_of_issue: Optional[str]
    tax_id_number: Optional[str]
    charter_capital: Optional[float]
    date_of_listing: Optional[str]
    exchange: Optional[str]
    initial_listing_price: Optional[float]
    listing_volume: Optional[float]


# NOT YET IMPLEMENT
class DailyMetric(BaseModel):
    eps: float
    price_to_earnings: float
    price_to_book: float
    ev_to_ebit: float


class Company(BaseModel):
    id: Optional[str] = Field(default="ACB", alias="_id")
    icb_code: str
    company_name: str
    short_name: str
    international_name: str
    profile: Profile
    # daily_metrics: DailyMetric

    @staticmethod
    def get_collection_name():
        return "companies"

    class Config:
        populate_by_name = True


class CompanyRepository(AbstractRepository[Company]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "companies"
