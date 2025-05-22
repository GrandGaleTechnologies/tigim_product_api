from fastapi import APIRouter

from app.core.tags import RouteTags
from app.store.routes.base import router as base_router
from app.store.routes.product import router as product_router

# Globals
router = APIRouter()
tags = RouteTags()

# Routes
router.include_router(base_router, prefix="/stores")
router.include_router(product_router, prefix="/stores/{store_id}/products")
