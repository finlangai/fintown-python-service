import sys

# DISABLE CACHE
sys.dont_write_bytecode = True

from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES
load_dotenv()
### ================================================================================
### ================================END SYSTEM CONFIG===============================
### ================================================================================

from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FinTown Python Service",
    version="369",
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


from app.routers import stocks

app.include_router(stocks.router)
