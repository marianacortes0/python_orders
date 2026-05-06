from __future__ import annotations
from fastapi import APIRouter

from src.routes.customer_routes import router as customer_router
from src.routes.health_routes import router as health_router
from src.routes.order_routes import router as order_router
from src.routes.product_routes import router as product_router
from src.routes.supplier_routes import router as supplier_router

router = APIRouter()
router.include_router(order_router)
router.include_router(customer_router)
router.include_router(product_router)
router.include_router(supplier_router)
router.include_router(health_router)
