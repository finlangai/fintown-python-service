from fastapi import APIRouter

router = APIRouter()

from app.routers.dtos import StockRequest


@router.post(
    "/stocks/request",
    name="Symbol Requesting",
    description="Demand a new stock symbol, when called, Python Service will seed and generate data for the Stock Symbol if it exists",
)
async def stock_request(req: StockRequest):
    return {"message": "Cum back later nigga, this is just the interface"}


from .dtos import RegenerateAssessment


@router.post(
    "/stocks/regenerate",
    name="Regenerate Assessment",
    description="Regenerate assessment for a specific metric of a stock symbol",
)
async def assessment_regenerate(req: RegenerateAssessment):
    return {"message": "Cum back later nigga, this is just the interface"}
