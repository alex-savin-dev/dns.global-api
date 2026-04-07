"""Shared test fixtures."""

import os

# Provide safe placeholder values for required settings BEFORE importing the
# app, so a fresh checkout (no .env) can still run the unit tests.
os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test"
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault(
    "CREDENTIAL_ENCRYPTION_KEY", "test-key-test-key-test-key-test-key-0123"
)
os.environ.setdefault("ENVIRONMENT", "development")

import pytest  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture
async def client():
    """Async HTTP test client backed by the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
