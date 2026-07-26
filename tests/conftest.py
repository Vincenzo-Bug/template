"""Shared deterministic test fixtures."""

from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.config import Environment, Settings
from app.main import create_app


class HealthyDatabase:
    """Database test double that is always ready."""

    async def ping(self) -> None:
        """Complete without error."""


@pytest.fixture
def settings() -> Settings:
    """Return settings isolated from developer environment files."""
    return Settings(
        _env_file=None,
        environment=Environment.TEST,
        app_name="Service Template Test",
        app_version="test",
        log_json=True,
    )


@pytest.fixture
def healthy_database() -> HealthyDatabase:
    """Return a healthy database test double."""
    return HealthyDatabase()


@pytest.fixture
def app(
    settings: Settings,
    healthy_database: HealthyDatabase,
) -> FastAPI:
    """Return an application with no external infrastructure."""
    return create_app(settings=settings, database=healthy_database)


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    """Return an asynchronous in-process API client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client
