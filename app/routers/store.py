from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_common_db_session
from ..repo.models import Brands, Stores, Products, Variations, Session

# initial router

router = APIRouter(
    prefix="/store",
    tags=["store"],
    dependencies=[Depends(get_common_db_session)]
)

CommonDBSession = Annotated[Session, Depends(get_common_db_session)]

@router.get("/")
async def get_test(db: CommonDBSession):
    return db.query(Stores).all()

@router.get("/brands")
async def get_brands(db: CommonDBSession):
    return db.query(Brands).all()

@router.get("/products/{brand_id}")
async def get_products(db: CommonDBSession, brand_id: int):
    return db.query(Products).filter(Products.brand_id==brand_id).all()

@router.get("/variation/{product_id}")
async def get_variations(db:CommonDBSession, product_id: int):
    variations = db.query(Variations).filter(Variations.product_id==product_id).all()
    if (variations.count == 0):
        return 0
    return variations