"""Async SQLAlchemy engine and transaction lifecycle."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings


class DatabaseManager:
    """Own the asynchronous database engine and session factory."""

    def __init__(self, settings: Settings) -> None:
        """Build a lazy SQLAlchemy engine from validated settings."""
        self._engine = create_async_engine(
            settings.database_url.get_secret_value(),
            echo=settings.database_echo,
            pool_pre_ping=True,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            connect_args={
                "timeout": settings.database_connect_timeout_seconds,
                "server_settings": {"application_name": "service-api"},
            },
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        """Expose the engine to migrations and controlled instrumentation."""
        return self._engine

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Provide a transactional session with automatic rollback on errors."""
        async with self._session_factory() as session, session.begin():
            yield session

    async def ping(self) -> None:
        """Verify that PostgreSQL accepts a simple query."""
        async with self._engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

    async def dispose(self) -> None:
        """Release all pooled database connections."""
        await self._engine.dispose()
