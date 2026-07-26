"""Liveness and readiness endpoints."""

import asyncio
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status

from app.api.dependencies import DatabaseHealthCheck, get_database
from app.core.config import Settings
from app.core.logging import get_logger
from app.schemas.health import DependencyStatus, HealthResponse, ReadinessResponse

router = APIRouter(tags=["operations"])
logger = get_logger(__name__)


def _settings(request: Request) -> Settings:
    return request.app.state.settings  # type: ignore[no-any-return]


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Process liveness",
)
async def health(request: Request) -> HealthResponse:
    """Report process liveness without contacting dependencies."""
    settings = _settings(request)
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        timestamp=datetime.now(UTC),
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ReadinessResponse}},
    summary="Service readiness",
)
async def readiness(
    request: Request,
    response: Response,
    database: Annotated[DatabaseHealthCheck, Depends(get_database)],
) -> ReadinessResponse:
    """Report whether required infrastructure is ready."""
    settings = _settings(request)
    database_status = "ok"
    overall_status = "ready"
    try:
        async with asyncio.timeout(settings.readiness_timeout_seconds):
            await database.ping()
    except Exception as error:  # noqa: BLE001 - adapter boundary must fail safely
        database_status = "unavailable"
        overall_status = "not_ready"
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        logger.warning(
            "readiness_check_failed",
            extra={"dependency": "postgresql", "error_type": type(error).__name__},
        )

    return ReadinessResponse(
        status=overall_status,
        service=settings.app_name,
        version=settings.app_version,
        timestamp=datetime.now(UTC),
        dependencies={"postgresql": DependencyStatus(status=database_status)},
    )
