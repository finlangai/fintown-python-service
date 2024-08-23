from pydantic import BaseModel


class RegenerateAssessment(BaseModel):
    symbol: str
    identifier: str
