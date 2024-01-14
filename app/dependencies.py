from typing import Annotated
from fastapi import Header, HTTPException
from .repo.database import Session

# dependencies goes here
# add JWT support here

async def get_common_db_session():
    return Session()