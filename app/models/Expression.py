from pydantic import BaseModel
from app.enums import ParamLocation


class Parameter(BaseModel):
    field: str
    slug: str
    location: ParamLocation
    # is_allow_zero: bool = True
    is_allow_negative: bool = False


class Expression(BaseModel):
    name: str
    expression: str
    parameters: list[Parameter]
