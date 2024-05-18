from fastapi import APIRouter

from .sqlite_route import router as crudRouter

from .auth import router as authRouter
from .token import router as tokenRouter

router = APIRouter()

router.include_router(
    crudRouter,
    prefix="/sqlite",
    tags=["sqlite-endpoint"],
)

router.include_router(
    authRouter,
    prefix="/auth",
    tags=["auth-endpoint"],
)

router.include_router(
    tokenRouter,
    prefix="/token",
    tags=["token-endpoint"],
)
