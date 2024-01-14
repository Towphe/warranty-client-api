from fastapi import APIRouter

# initial router

router = APIRouter()

@router.get("/")
async def index():
    return "Hello World!"