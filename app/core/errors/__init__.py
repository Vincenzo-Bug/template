"""Typed safe application errors."""

from app.core.errors.exceptions import AppError, ServiceUnavailableError
from app.core.errors.handlers import install_exception_handlers

__all__ = ["AppError", "ServiceUnavailableError", "install_exception_handlers"]
