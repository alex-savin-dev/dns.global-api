"""FastAPI application factory."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.config import settings
from app.core.exceptions import DnsGlobalError
from app.core.logging import get_logger, setup_logging
from app.core.middleware import register_middleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown lifecycle."""
    setup_logging()
    logger.info(
        "DNS.GLOBAL starting — env=%s version=%s",
        settings.environment,
        settings.app_version,
    )
    yield
    logger.info("DNS.GLOBAL shutting down")


def create_app() -> FastAPI:
    """Build and return the FastAPI application."""
    app = FastAPI(
        title="DNS.GLOBAL",
        description="API-first DNS automation service",
        version=settings.app_version,
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
        lifespan=lifespan,
    )

    # Middleware
    register_middleware(app)

    # Routers
    app.include_router(api_router)

    # Global exception handler for DnsGlobalError
    @app.exception_handler(DnsGlobalError)
    async def dns_global_error_handler(
        request: Request, exc: DnsGlobalError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )

    return app


app = create_app()
