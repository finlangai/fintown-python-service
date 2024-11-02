from starlette.responses import StreamingResponse
from fastapi import APIRouter

from app.utils import stream_function_output
import jobs
import jobs.refresh
import jobs.refresh.stash_stats
import jobs.refresh.stock_quotes

router = APIRouter()


@router.post("/refresh/stash_stats")
async def refresh_stash_stats():

    closure_func = jobs.refresh.stash_stats.get_closure()
    return StreamingResponse(
        stream_function_output(closure_func),
        media_type="text/event-stream",
    )


@router.post("/refresh/stock_quotes")
async def refresh_stock_quotes():

    closure_func = jobs.refresh.stock_quotes.get_closure()
    return StreamingResponse(
        stream_function_output(closure_func),
        media_type="text/event-stream",
    )
