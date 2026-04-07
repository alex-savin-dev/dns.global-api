"""Tests for the health check endpoint."""

import pytest


@pytest.mark.asyncio
async def test_healthz_returns_ok(client):
    """GET /healthz should return 200 with status and version."""
    response = await client.get("/healthz")
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_healthz_content_type(client):
    """GET /healthz should return application/json."""
    response = await client.get("/healthz")
    assert "application/json" in response.headers["content-type"]
