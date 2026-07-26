"""Safe structured JSON logging built on the Python standard library."""

import json
import logging
import re
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

_SENSITIVE_KEYS = frozenset(
    {
        "authorization",
        "cookie",
        "database_url",
        "password",
        "private_key",
        "redis_url",
        "secret",
        "seed_phrase",
        "token",
    }
)
_CREDENTIAL_PATTERN = re.compile(r"(?P<scheme>[a-z][a-z0-9+.-]*://)[^@\s]+@", re.I)


def _redact(value: Any, key: str | None = None) -> Any:
    """Recursively redact values whose names or shapes are sensitive."""
    if key is not None and key.lower() in _SENSITIVE_KEYS:
        return "[REDACTED]"
    if isinstance(value, Mapping):
        return {
            str(item_key): _redact(item, str(item_key))
            for item_key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [_redact(item) for item in value]
    if isinstance(value, str):
        return _CREDENTIAL_PATTERN.sub(r"\g<scheme>[REDACTED]@", value)
    return value


class JsonFormatter(logging.Formatter):
    """Render allowlisted log record attributes as one JSON object."""

    _standard_attributes = frozenset(
        logging.LogRecord(
            name="",
            level=0,
            pathname="",
            lineno=0,
            msg="",
            args=(),
            exc_info=None,
        ).__dict__
    )

    def format(self, record: logging.LogRecord) -> str:
        """Format a record without leaking exception arguments or credentials."""
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in self._standard_attributes and not key.startswith("_"):
                payload[key] = _redact(value, key)
        if record.exc_info is not None and record.exc_info[0] is not None:
            payload["exception_type"] = record.exc_info[0].__name__
        return json.dumps(_redact(payload), separators=(",", ":"), default=str)


def configure_logging(*, level: str, json_output: bool) -> None:
    """Configure the root logger with safe process-wide defaults."""
    handler = logging.StreamHandler()
    if json_output:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level.upper())


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced standard-library logger."""
    return logging.getLogger(name)
