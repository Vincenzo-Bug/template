"""Configuration safety tests."""

import pytest
from pydantic import SecretStr, ValidationError

from app.core.config import Environment, Settings


def test_default_secret_representations_are_redacted() -> None:
    """Configuration representations must not expose connection credentials."""
    settings = Settings(_env_file=None)

    representation = repr(settings)

    assert "service_dev_only" not in representation
    assert "**********" in representation


def test_cors_origins_are_normalized() -> None:
    """Comma-separated origins become a trimmed immutable tuple."""
    settings = Settings(
        _env_file=None,
        cors_origins="https://a.example, https://b.example ,,",
    )

    assert settings.cors_origin_list == (
        "https://a.example",
        "https://b.example",
    )


@pytest.mark.parametrize("environment", ["invalid", "", "prod"])
def test_unknown_environment_is_rejected(environment: str) -> None:
    """Unknown environment labels must fail startup validation."""
    with pytest.raises(ValidationError):
        Settings(_env_file=None, environment=environment)


def test_debug_is_rejected_in_production() -> None:
    """Production debug mode must fail closed."""
    with pytest.raises(ValidationError, match="debug must be disabled"):
        Settings(
            _env_file=None,
            environment=Environment.PRODUCTION,
            debug=True,
            database_url=SecretStr(
                "postgresql+asyncpg://service:strong@database:5432/service"
            ),
        )


def test_development_credentials_are_rejected_in_production() -> None:
    """Known development database credentials must not start in production."""
    with pytest.raises(ValidationError, match="development database credentials"):
        Settings(
            _env_file=None,
            environment=Environment.PRODUCTION,
            database_url=SecretStr(
                "postgresql+asyncpg://service_dev:service_dev_only@database:5432/service"
            ),
        )


def test_wildcard_cors_is_rejected_in_production() -> None:
    """Credential-bearing production origins cannot be wildcarded."""
    with pytest.raises(ValidationError, match="wildcard CORS"):
        Settings(
            _env_file=None,
            environment=Environment.PRODUCTION,
            database_url=SecretStr(
                "postgresql+asyncpg://service:strong@database:5432/service"
            ),
            cors_origins="*",
        )
