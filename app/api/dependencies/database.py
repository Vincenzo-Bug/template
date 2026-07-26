"""Database-related API dependencies."""

from typing import Protocol, cast

from fastapi import Request


class DatabaseHealthCheck(Protocol):
    """Minimal database behavior needed by readiness."""

    async def ping(self) -> None:
        """Raise when the database is unavailable."""


async def get_database(request: Request) -> DatabaseHealthCheck:
    """Return the application-scoped database health adapter."""
    return cast(DatabaseHealthCheck, request.app.state.database)
