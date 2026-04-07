"""Structured JSON logging setup.

Every log entry includes: timestamp, level, request_id, module name.
Secret redaction: never log full API keys, tokens, or credentials.
"""

import logging
import re
import sys

from pythonjsonlogger.json import JsonFormatter

from app.config import settings

# Patterns to redact from log output
_REDACT_PATTERNS = [
    (re.compile(r"(sk_live_)[A-Za-z0-9]+"), r"\1***"),
    (re.compile(r"(pk_live_)[A-Za-z0-9]+"), r"\1***"),
    (re.compile(r"(sess_)[A-Za-z0-9]+"), r"\1***"),
    (re.compile(r"(Bearer\s+)[A-Za-z0-9._\-]+"), r"\1***"),
    (re.compile(r"(token[\"']?\s*[:=]\s*[\"']?)[A-Za-z0-9._\-]+"), r"\1***"),
    (re.compile(r"(password[\"']?\s*[:=]\s*[\"']?)[^\s\"']+"), r"\1***"),
    (re.compile(r"(credential_encryption_key[\"']?\s*[:=]\s*[\"']?)[^\s\"']+"), r"\1***"),
]


def _redact(message: str) -> str:
    """Redact sensitive values from a log message."""
    for pattern, replacement in _REDACT_PATTERNS:
        message = pattern.sub(replacement, message)
    return message


class RedactingJsonFormatter(JsonFormatter):
    """JSON formatter that redacts secrets and adds standard fields."""

    def add_fields(
        self,
        log_record: dict,
        record: logging.LogRecord,
        message_dict: dict,
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["level"] = record.levelname
        log_record["module"] = record.module
        log_record["logger"] = record.name
        # request_id is injected via middleware into the log record extras
        if not log_record.get("request_id"):
            log_record["request_id"] = None

    def format(self, record: logging.LogRecord) -> str:
        # Redact the message itself
        record.msg = _redact(str(record.msg))
        return super().format(record)


def setup_logging() -> None:
    """Configure root logger with structured JSON output."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = RedactingJsonFormatter(
        fmt="%(timestamp)s %(level)s %(name)s %(message)s",
        rename_fields={"timestamp": "timestamp", "levelname": "level"},
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.log_level.upper())

    # Honour LOG_LEVEL for noisy third-party loggers in development so the
    # operator can opt into DEBUG/INFO when they need it; in non-development
    # environments cap them at WARNING to keep production logs clean.
    app_level = logging.getLevelName(settings.log_level.upper())
    if not isinstance(app_level, int):
        app_level = logging.INFO
    if settings.environment == "development":
        noisy_level = app_level
    else:
        noisy_level = max(app_level, logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(noisy_level)
    logging.getLogger("sqlalchemy.engine").setLevel(noisy_level)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger."""
    return logging.getLogger(name)
