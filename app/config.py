"""Application configuration via pydantic-settings.

All settings are loaded from environment variables. See .env.example for documentation.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """DNS.GLOBAL application settings.

    Loaded from environment variables. Prefix-free for simplicity;
    all vars are documented in .env.example.
    """

    # --- Database (REQUIRED — no default; misconfigured deploys must fail fast) ---
    database_url: str

    # --- Redis (REQUIRED) ---
    redis_url: str

    # --- Security (REQUIRED) ---
    credential_encryption_key: str  # AES-256 key, Phase 1 from env var

    # --- Environment ---
    environment: str = "development"  # development | staging | production

    # --- CORS ---
    # Stored as comma-separated string because pydantic-settings v2 dotenv source
    # cannot coerce empty strings into list[str]. Use cors_origins_list to consume.
    cors_allowed_origins: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse cors_allowed_origins into a list."""
        if not self.cors_allowed_origins.strip():
            return []
        return [o.strip() for o in self.cors_allowed_origins.split(",") if o.strip()]

    # --- Rate limiting ---
    api_rate_limit: int = 100  # requests per minute per IP

    # --- Logging ---
    log_level: str = "INFO"

    # --- App metadata ---
    app_version: str = "0.1.0"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Singleton settings instance — import this from other modules
settings = Settings()  # type: ignore[call-arg]
