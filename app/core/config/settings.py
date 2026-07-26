"""Validated application settings loaded from the environment."""

from functools import lru_cache
from pathlib import Path
from typing import Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str):
    """Supported runtime environment names."""

    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Runtime settings for the service template.

    Secrets use ``SecretStr`` so their representations are redacted. Application
    code must unwrap them only at the infrastructure boundary that needs them.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SERVICE_",
        extra="forbid",
        case_sensitive=False,
    )

    environment: str = Environment.DEVELOPMENT
    app_name: str = "Service Template"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"
    log_json: bool = True

    database_url: SecretStr = SecretStr(
        "postgresql+asyncpg://service_dev:service_dev_only@localhost:5432/service"
    )
    database_echo: bool = False
    database_pool_size: int = Field(default=5, ge=1, le=50)
    database_max_overflow: int = Field(default=5, ge=0, le=50)
    database_connect_timeout_seconds: float = Field(default=5.0, gt=0, le=30)

    redis_url: SecretStr = SecretStr("redis://localhost:6379/0")
    readiness_timeout_seconds: float = Field(default=2.0, gt=0, le=10)
    cors_origins: str = ""

    otel_enabled: bool = False
    otel_service_name: str = "service-api"
    otel_exporter_otlp_endpoint: str | None = None

    @model_validator(mode="after")
    def validate_environment_safety(self) -> Self:
        """Reject production settings that weaken safe defaults."""
        allowed = {
            Environment.DEVELOPMENT,
            Environment.TEST,
            Environment.STAGING,
            Environment.PRODUCTION,
        }
        if self.environment not in allowed:
            msg = f"environment must be one of {sorted(allowed)}"
            raise ValueError(msg)

        if self.environment == Environment.PRODUCTION:
            if self.debug:
                raise ValueError("debug must be disabled in production")
            if "*" in self.cors_origin_list:
                raise ValueError("wildcard CORS origins are forbidden in production")
            database_url = self.database_url.get_secret_value()
            if "service_dev_only" in database_url:
                raise ValueError("development database credentials are forbidden")
        return self

    @property
    def cors_origin_list(self) -> tuple[str, ...]:
        """Return normalized configured CORS origins."""
        return tuple(
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        )

    @property
    def project_root(self) -> Path:
        """Return the application project root."""
        return Path(__file__).resolve().parents[3]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and cache validated settings for the process."""
    return Settings()
