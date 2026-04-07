FROM python:3.13-slim-bookworm

WORKDIR /app

# Install Python deps from pyproject.toml (single source of truth)
COPY pyproject.toml README.md ./
COPY app ./app
RUN pip install --no-cache-dir .

# Copy the rest of the project (configs, alembic.ini, etc.)
COPY . .

EXPOSE 8000

# Run migrations then start the server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
