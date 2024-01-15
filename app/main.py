from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

# import from dependecies
from .dependencies import get_common_db_session
from .routers import store
from .repo.database import Session
from .repo.models import Variations
import os

api_app = FastAPI(title="api app")

api_app.include_router(store.router)

@api_app.get("/api")
async def index():
    return {
        "title" : "Welcome to warranty site API",
        "description" : "This is a development API that provides data to the client website of a warranty forms"
    }
    
app = FastAPI(title="main app")

app.mount("/api", api_app)    
app.mount("/", StaticFiles(directory=os.path.dirname(__file__) + "\\views", html=True), name="views")