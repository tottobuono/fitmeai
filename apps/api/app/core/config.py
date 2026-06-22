"""Configurazione applicativa, letta da env var (vedi `.env.example`).

Tutti i valori hanno default sensati per lo sviluppo locale, cosi' import e test non
richiedono un `.env`. In produzione i valori arrivano dall'ambiente/secrets manager.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    env: str = "local"

    # Persistenza / coda
    database_url: str = "postgresql+psycopg://fitme:change-me-in-local@localhost:5432/fitme"
    redis_url: str = "redis://localhost:6379/0"
    redis_queue_name: str = "fitme:tryon:jobs"

    # Try-on
    tryon_provider: str = "mock"

    # API
    api_port: int = 8000
    cors_allow_origins: str = "http://localhost:3000"

    # Logging
    log_level: str = "info"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
