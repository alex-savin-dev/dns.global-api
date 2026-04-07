FROM python:3.13-slim-bookworm

WORKDIR /app

# Python deps — install directly (no apt-get needed)
COPY pyproject.toml ./
RUN pip install --no-cache-dir \
    "fastapi>=0.135.0,<1.0" \
    "uvicorn[standard]>=0.44.0" \
    "sqlalchemy[asyncio]>=2.0.49" \
    "asyncpg>=0.31.0" \
    "alembic>=1.18.0" \
    "pydantic>=2.12.0" \
    "pydantic-settings>=2.13.0" \
    "dnspython>=2.8.0" \
    "redis>=7.1.0" \
    "cryptography>=46.0.0" \
    "httpx>=0.28.0" \
    "python-json-logger>=3.3.0" \
    "bcrypt>=4.3.0"

# Application code
COPY . .

EXPOSE 8000

# Run migrations then start the server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
