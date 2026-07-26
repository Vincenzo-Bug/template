"""Safe HTTP error translation tests."""

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.errors import AppError, install_exception_handlers


def _error_app() -> FastAPI:
    app = FastAPI()
    install_exception_handlers(app)

    @app.get("/expected")
    async def expected_error() -> None:
        raise AppError(
            code="test_rejection", detail="Safe explanation.", status_code=409
        )

    @app.get("/unexpected")
    async def unexpected_error() -> None:
        raise RuntimeError("database password must never leave the boundary")

    return app


async def test_expected_error_uses_problem_details() -> None:
    """Expected application errors should preserve their safe public detail."""
    transport = ASGITransport(app=_error_app(), raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/expected")

    assert response.status_code == 409
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["code"] == "test_rejection"
    assert response.json()["detail"] == "Safe explanation."


async def test_unexpected_error_is_sanitized() -> None:
    """Unexpected exceptions must not disclose their internal message."""
    transport = ASGITransport(app=_error_app(), raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/unexpected")

    assert response.status_code == 500
    assert response.json()["code"] == "internal_error"
    assert "database password" not in response.text
