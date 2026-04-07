FROM python:3.13-slim-bookworm

WORKDIR /app

# Copy the project and install once from pyproject.toml (single source of truth)
COPY . .
RUN pip install --no-cache-dir .

EXPOSE 8000

# Run migrations then start the server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
