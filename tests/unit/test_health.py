"""Health and readiness API tests."""

import asyncio

from httpx import ASGITransport, AsyncClient, Response

from app.core.config import Environment, Settings
from app.main import create_app


class ExplodingDatabase:
    """Database double that proves liveness performs no I/O."""

    async def ping(self) -> None:
        """Raise if called."""
        raise AssertionError("liveness must not call the database")


class UnavailableDatabase:
    """Database double representing a failed dependency."""

    async def ping(self) -> None:
        """Raise a safe infrastructure failure."""
        raise RuntimeError("sensitive database failure")


class SlowDatabase:
    """Database double representing an unbounded dependency."""

    async def ping(self) -> None:
        """Sleep longer than the configured readiness deadline."""
        await asyncio.sleep(0.1)


async def _request(
    database: object,
    path: str,
    *,
    readiness_timeout: float = 0.05,
    correlation_id: str | None = None,
) -> Response:
    settings = Settings(
        _env_file=None,
        environment=Environment.TEST,
        app_name="Service Template Test",
        app_version="test",
        readiness_timeout_seconds=readiness_timeout,
    )
    app = create_app(settings=settings, database=database)
    transport = ASGITransport(app=app)
    headers = (
        {"X-Correlation-ID": correlation_id} if correlation_id is not None else None
    )
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get(path, headers=headers)


async def test_health_is_live_without_database() -> None:
    """Liveness must be fast and independent from PostgreSQL."""
    response = await _request(ExplodingDatabase(), "/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "Service Template Test"
    assert response.json()["version"] == "test"
    assert "timestamp" in response.json()


async def test_readiness_reports_healthy_database(client: AsyncClient) -> None:
    """Readiness must report a healthy required database."""
    response = await client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["dependencies"] == {"postgresql": {"status": "ok"}}


async def test_readiness_fails_safely_when_database_is_unavailable() -> None:
    """Dependency errors must be sanitized and return 503."""
    response = await _request(UnavailableDatabase(), "/ready")

    body = response.json()
    assert response.status_code == 503
    assert body["status"] == "not_ready"
    assert body["dependencies"] == {"postgresql": {"status": "unavailable"}}
    assert "sensitive database failure" not in response.text


async def test_readiness_timeout_is_bounded() -> None:
    """A slow dependency must not block readiness indefinitely."""
    response = await _request(
        SlowDatabase(),
        "/ready",
        readiness_timeout=0.01,
    )

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"


async def test_correlation_id_is_returned(client: AsyncClient) -> None:
    """A safe caller correlation ID should be preserved."""
    correlation_id = "01J3AGM9A7J83B7EKJCF8Q8K3Z"

    response = await client.get(
        "/health",
        headers={"X-Correlation-ID": correlation_id},
    )

    assert response.headers["X-Correlation-ID"] == correlation_id


async def test_invalid_correlation_id_is_replaced(client: AsyncClient) -> None:
    """Untrusted correlation identifiers must not be reflected."""
    response = await client.get(
        "/health",
        headers={"X-Correlation-ID": "contains spaces and is not safe"},
    )

    assert response.headers["X-Correlation-ID"] != "contains spaces and is not safe"
