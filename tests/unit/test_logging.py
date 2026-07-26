"""Structured logging and redaction tests."""

import json
import logging

from app.core.logging.configuration import JsonFormatter


def test_json_formatter_redacts_named_secrets_and_dsn_credentials() -> None:
    """Structured records must redact secret fields and URL credentials."""
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="connection failed for postgresql://user:password@database/service",
        args=(),
        exc_info=None,
    )
    record.database_url = "postgresql://user:password@database/service"
    record.context = {"authorization": "Bearer secret", "safe": "value"}

    payload = json.loads(formatter.format(record))

    assert "password" not in payload["event"]
    assert payload["database_url"] == "[REDACTED]"
    assert payload["context"]["authorization"] == "[REDACTED]"
    assert payload["context"]["safe"] == "value"


def test_json_formatter_records_exception_type_without_message() -> None:
    """Exception details must not leak through structured logs."""
    formatter = JsonFormatter()
    try:
        raise RuntimeError("secret failure detail")
    except RuntimeError:
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname=__file__,
            lineno=1,
            msg="operation_failed",
            args=(),
            exc_info=__import__("sys").exc_info(),
        )

    payload = json.loads(formatter.format(record))

    assert payload["exception_type"] == "RuntimeError"
    assert "secret failure detail" not in formatter.format(record)
