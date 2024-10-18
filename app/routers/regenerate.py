from starlette.responses import StreamingResponse
from fastapi import APIRouter, HTTPException

from app.utils import stream_function_output
import jobs
import jobs.regenerate
import jobs.regenerate.assessment

router = APIRouter()


@router.post("/regenerate/assessment")
async def regenerate_assessment(symbol: str):
    if symbol is None:
        raise HTTPException(
            status_code=400, detail="symbol query parameter is required"
        )

    closure_func = jobs.regenerate.assessment.get_closure(symbol=symbol)
    return StreamingResponse(
        stream_function_output(closure_func),
        media_type="text/event-stream",
    )
