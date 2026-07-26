"""Tests proving the starter exposes only operational endpoints."""

from httpx import AsyncClient


async def test_only_operational_routes_exist(
    client: AsyncClient,
) -> None:
    """New projects start with health endpoints and add product routes explicitly."""
    response = await client.get("/openapi.json")
    visible_paths = set(response.json()["paths"])

    assert visible_paths == {"/health", "/ready"}
