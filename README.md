# DNS.GLOBAL

API-first DNS automation service. Enables SaaS apps to programmatically deploy DNS records without user intervention at registrars.

## Quick Start (Local Development)

```bash
# 1. Copy environment file
cp .env.example .env
# Fill in CREDENTIAL_ENCRYPTION_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")

# 2. Start all services
docker-compose up

# 3. Verify
curl http://localhost:8000/healthz
# → {"status": "ok", "version": "0.1.0"}
```

## Architecture

- **FastAPI** — async Python web framework
- **PostgreSQL 15** — primary datastore (via SQLAlchemy async + asyncpg)
- **Redis 7** — job queue for async operations
- **Alembic** — database migrations

## Project Structure

```
dns-global/
├── app/
│   ├── main.py           # FastAPI app factory
│   ├── config.py          # pydantic-settings configuration
│   ├── database.py        # SQLAlchemy async engine
│   ├── api/               # FastAPI routers
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic request/response schemas
│   ├── services/          # Business logic
│   ├── adapters/          # DNS provider adapters
│   ├── core/              # Middleware, exceptions, logging
│   └── migrations/        # Alembic migrations
├── tests/
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## Deployment

Hosted on Railway with static outbound IP. Domain: dns.global.
