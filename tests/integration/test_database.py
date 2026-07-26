"""PostgreSQL integration tests."""

import os

import pytest
from pydantic import SecretStr
from sqlalchemy import text

from app.core.config import Environment, Settings
from app.infrastructure.database import DatabaseManager


def _integration_database_url() -> str:
    url = os.getenv("SERVICE_TEST_DATABASE_URL")
    if url is None:
        pytest.skip("SERVICE_TEST_DATABASE_URL is not configured")
    return url


@pytest.mark.integration
async def test_database_ping_and_transaction() -> None:
    """The async engine must connect and commit a transaction."""
    settings = Settings(
        _env_file=None,
        environment=Environment.TEST,
        database_url=SecretStr(_integration_database_url()),
    )
    database = DatabaseManager(settings)
    try:
        await database.ping()
        async with database.session() as session:
            value = await session.scalar(text("SELECT 1"))
        assert value == 1
    finally:
        await database.dispose()
