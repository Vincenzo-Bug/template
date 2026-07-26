"""Application error types safe to translate at the HTTP boundary."""


class AppError(Exception):
    """Base class for expected application errors."""

    def __init__(self, *, code: str, detail: str, status_code: int) -> None:
        """Initialize a safe error."""
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.status_code = status_code


class ServiceUnavailableError(AppError):
    """A required service is not ready."""

    def __init__(self, *, code: str = "service_unavailable") -> None:
        """Initialize a non-disclosing availability error."""
        super().__init__(
            code=code,
            detail="A required service is temporarily unavailable.",
            status_code=503,
        )
