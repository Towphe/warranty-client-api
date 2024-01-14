from fastapi import Depends, FastAPI

# import from dependecies
from .routers import products

app = FastAPI()
# configure https later

app.include_router(products.router)

