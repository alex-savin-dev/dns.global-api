"""Root router — aggregates all sub-routers."""

from fastapi import APIRouter

from app.api.health import router as health_router

api_router = APIRouter()

# Health check (no prefix — serves at /healthz)
api_router.include_router(health_router, tags=["health"])
