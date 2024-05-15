from fastapi import APIRouter, Depends
from app.api.models.model1 import Model1

router = APIRouter()


@router.post("/", response_model=Model1)
async def create_item(item: Model1):
    # Implement your logic here
    return item
