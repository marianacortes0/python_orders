from fastapi import APIRouter

from src.routes.order_routes import router as order_router

router = APIRouter(prefix="/api/v1")
router.include_router(order_router)
