"""FastAPI exception translation with safe problem details."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.errors.exceptions import AppError
from app.core.logging import get_logger

logger = get_logger(__name__)


class ProblemDetail(BaseModel):
    """RFC 9457-inspired safe API error body."""

    type: str = "about:blank"
    title: str
    status: int
    code: str
    detail: str
    instance: str
    correlation_id: str | None = None


def _problem_response(
    request: Request,
    *,
    status_code: int,
    code: str,
    title: str,
    detail: str,
) -> JSONResponse:
    correlation_id = getattr(request.state, "correlation_id", None)
    problem = ProblemDetail(
        title=title,
        status=status_code,
        code=code,
        detail=detail,
        instance=request.url.path,
        correlation_id=correlation_id,
    )
    return JSONResponse(
        status_code=status_code,
        content=problem.model_dump(mode="json"),
        media_type="application/problem+json",
    )


def install_exception_handlers(app: FastAPI) -> None:
    """Install expected and last-resort exception handlers."""

    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, error: AppError) -> JSONResponse:
        logger.info(
            "request_rejected",
            extra={"error_code": error.code, "status_code": error.status_code},
        )
        return _problem_response(
            request,
            status_code=error.status_code,
            code=error.code,
            title="Request could not be completed",
            detail=error.detail,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(
        request: Request,
        error: Exception,
    ) -> JSONResponse:
        logger.exception(
            "unexpected_request_error",
            extra={"error_type": type(error).__name__},
        )
        return _problem_response(
            request,
            status_code=500,
            code="internal_error",
            title="Internal server error",
            detail="The request could not be completed.",
        )
