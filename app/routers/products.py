from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_common_db_session
from ..repo.models import Variations, Session

# initial router

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_common_db_session)]
)

CommonDBSession = Annotated[Session, Depends(get_common_db_session)]

@router.get("/")
async def get_test(db: CommonDBSession):
    return db.query(Variations)