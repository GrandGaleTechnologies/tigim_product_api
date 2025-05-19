from fastapi import APIRouter

from app.core.tags import RouteTags
from app.client.routes.base import router as base_router

# Globals
router = APIRouter()
tags = RouteTags()

# Routes
router.include_router(base_router, prefix="/clients")
