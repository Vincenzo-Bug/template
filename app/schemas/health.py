"""Health endpoint response schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Liveness response."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]
    service: str
    version: str
    timestamp: datetime


class DependencyStatus(BaseModel):
    """Safe readiness state for a dependency."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok", "unavailable"]


class ReadinessResponse(BaseModel):
    """Readiness response without infrastructure details."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ready", "not_ready"]
    service: str
    version: str
    timestamp: datetime
    dependencies: dict[str, DependencyStatus]
