from pydantic import BaseModel


class Profile(BaseModel):
    head_quarters: str
    phone: str
    fax: str
    email: str
    web_address: str
    employees: int
    business_license_number: str
    date_of_issue: str
    tax_id_number: str
    charter_capital: float
    date_of_listing: str
    exchange: str
    initial_listing_price: float
    listing_volume: float


# NOT YET IMPLEMENT
class DailyMetric(BaseModel):
    eps: float
    price_to_earnings: float
    price_to_book: float
    ev_to_ebit: float


class Company(BaseModel):
    icb_code: str
    company_name: str
    short_name: str
    international_name: str
    profile: Profile
    # daily_metrics: DailyMetric

    @staticmethod
    def get_collection_name():
        return "companies"
