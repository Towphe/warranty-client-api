from typing import Annotated
from fastapi import Depends, FastAPI

# import from dependecies
from .dependencies import get_common_db_session
from .routers import products
from .repo.database import Session
from .repo.models import Variations

app = FastAPI()

app.include_router(products.router)

@app.get("/")
async def index():
    return {
        "title" : "Welcome to warranty site API",
        "description" : "This is a development API that provides data to the client website of a warranty forms"
    }