"""FastAPI application assembly for the service template."""

import re
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health_router
from app.core.config import Settings, get_settings
from app.core.errors import install_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.infrastructure.database import DatabaseManager
from app.infrastructure.observability import configure_telemetry

logger = get_logger(__name__)
_CORRELATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


def create_app(
    settings: Settings | None = None,
    database: DatabaseManager | Any | None = None,
) -> FastAPI:
    """Create an application with explicit replaceable infrastructure."""
    runtime_settings = settings or get_settings()
    configure_logging(
        level=runtime_settings.log_level,
        json_output=runtime_settings.log_json,
    )
    database_manager = database or DatabaseManager(runtime_settings)
    owns_database = database is None

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        logger.info(
            "application_started",
            extra={
                "environment": runtime_settings.environment,
                "version": runtime_settings.app_version,
            },
        )
        yield
        if owns_database:
            await application.state.database.dispose()
        logger.info("application_stopped")

    application = FastAPI(
        title=runtime_settings.app_name,
        version=runtime_settings.app_version,
        debug=runtime_settings.debug,
        lifespan=lifespan,
        docs_url="/docs" if runtime_settings.environment != "production" else None,
        redoc_url=None,
    )
    application.state.settings = runtime_settings
    application.state.database = database_manager

    @application.middleware("http")
    async def correlation_id_middleware(
        request: Request,
        call_next: Any,
    ) -> Any:
        correlation_id = request.headers.get("X-Correlation-ID")
        if (
            correlation_id is None
            or _CORRELATION_ID_PATTERN.fullmatch(correlation_id) is None
        ):
            correlation_id = str(uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

    if runtime_settings.cors_origin_list:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=list(runtime_settings.cors_origin_list),
            allow_credentials=False,
            allow_methods=["GET"],
            allow_headers=["Accept", "Content-Type", "X-Correlation-ID"],
        )

    install_exception_handlers(application)
    application.include_router(health_router)
    configure_telemetry(application, runtime_settings)
    return application


app = create_app()


def run() -> None:
    """Run the local development API server."""
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        access_log=False,
    )


if __name__ == "__main__":
    run()
