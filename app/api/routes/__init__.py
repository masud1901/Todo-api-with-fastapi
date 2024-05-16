from fastapi import APIRouter

from .sqlite_route import router as route1_router

# from .route2 import router as route2_router

router = APIRouter()

router.include_router(
    route1_router,
    prefix="/sqlite",
    tags=["sqlite-endpoint"],
)
# router.include_router(route2_router, prefix="/route2", tags=["Route 2"])
