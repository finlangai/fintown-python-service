from pydantic import BaseModel


class Holder(BaseModel):
    name: str
    position: str
    shares: int
    ownership: float
    is_organization: bool
    is_foreigner: bool
    is_founder: bool
