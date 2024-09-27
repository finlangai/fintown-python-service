from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import AbstractRepository
from pymongo.database import Database

from typing import Optional
from bson import ObjectId

from core.mongodb import get_database


class CompanyDelta(BaseModel):
    delta_in_week: Optional[float]
    delta_in_month: Optional[float]
    delta_in_year: Optional[float]


class Summary(BaseModel):
    company_profile: Optional[str]
    history_dev: Optional[str]
    company_promise: Optional[str]
    business_risk: Optional[str]
    key_developments: Optional[str]
    business_strategies: Optional[str]


class Profile(BaseModel):
    short_name: str
    international_name: str
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
    market_cap: Optional[float]


class Company(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    symbol: str
    icb_code: str
    company_name: str
    industry: str
    delta: CompanyDelta
    profile: Profile
    summary: Summary

    @field_validator("id", mode="before")
    def set_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class CompanyRepository(AbstractRepository[Company]):
    def __init__(self, database: Database = get_database()):
        super().__init__(database)

    class Meta:
        collection_name = "companies"
