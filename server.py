import sys

# DISABLE CACHE
# sys.dont_write_bytecode = True

from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES
load_dotenv()
### ================================================================================
### ================================END SYSTEM CONFIG===============================
### ================================================================================

from fastapi import FastAPI, responses, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FinTown Python Service",
    version="1",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # You can specify the methods you want to allow
    allow_headers=["*"],  # You can specify the headers you want to allow
)


@app.get("/")
def read_root():
    return responses.RedirectResponse(url="/docs")


from app.routers import stocks, regenerate

app.include_router(stocks.router)
app.include_router(regenerate.router)

# =============================================
# =========== BELOW IS FOR TESTING ============
# =============================================


from starlette.responses import StreamingResponse
from app.utils import stream_function_output
from jobs import inw


@app.get("/stream")
async def stream():
    return StreamingResponse(
        stream_function_output(inw.exec), media_type="text/event-stream"
    )
