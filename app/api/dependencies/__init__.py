"""FastAPI dependency providers."""

from app.api.dependencies.database import DatabaseHealthCheck, get_database

__all__ = ["DatabaseHealthCheck", "get_database"]
