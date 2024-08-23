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

app = FastAPI(
    title="FinTown Python Service",
    version="369",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)


@app.get("/")
def read_root():
    return responses.RedirectResponse(url="/docs")


from app.routers import stocks

app.include_router(stocks.router)
