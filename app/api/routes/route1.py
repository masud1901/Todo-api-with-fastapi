from fastapi import APIRouter, Depends
from app.api.models.models import Base

router = APIRouter()


# @router.post("/", response_model=Base)
# async def create_item(item: Base): # type: ignore
#     # Implement your logic here
#     return item
