"""Health check endpoint."""

from fastapi import APIRouter

from app.config import settings

router = APIRouter()


@router.get("/healthz")
async def healthz() -> dict:
    """Liveness / readiness probe.

    Returns 200 with version info. Used by Railway, Docker, and monitoring.
    """
    return {"status": "ok", "version": settings.app_version}
