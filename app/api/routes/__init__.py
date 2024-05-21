from fastapi import APIRouter

from .crud import router as crudRouter

from .auth import router as authRouter
from .token import router as tokenRouter
from .admin import router as adminRouter
from .user import router as userRouter

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


router.include_router(
    adminRouter,
    prefix="/admin",
    tags=["admin-endpoint"],
)

router.include_router(
    userRouter,
    prefix="/user",
    tags=["user-endpoint"],
)
