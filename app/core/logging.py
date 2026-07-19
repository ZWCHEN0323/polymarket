"""Structured JSON logging configuration for Cloud Logging compatibility."""

import logging
import sys
from datetime import UTC, datetime
from typing import Any

from pythonjsonlogger import json as json_logger

from app.core.constants import APP_NAME, DEFAULT_LOG_LEVEL


class CloudLoggingJsonFormatter(json_logger.JsonFormatter):
    """Format log records as JSON with Google Cloud Logging severity mapping."""

    SEVERITY_MAP: dict[int, str] = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO",
        logging.WARNING: "WARNING",
        logging.ERROR: "ERROR",
        logging.CRITICAL: "CRITICAL",
    }

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        """Add standard fields expected by Google Cloud Logging."""
        super().add_fields(log_record, record, message_dict)
        log_record["severity"] = self.SEVERITY_MAP.get(record.levelno, "DEFAULT")
        created_at = datetime.fromtimestamp(record.created, tz=UTC)
        log_record["timestamp"] = created_at.isoformat()
        log_record["logger"] = record.name
        log_record["service"] = APP_NAME


def setup_logging(log_level: str = DEFAULT_LOG_LEVEL) -> None:
    """Configure root logger with JSON output to stdout."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        CloudLoggingJsonFormatter(
            "%(timestamp)s %(severity)s %(name)s %(message)s",
        ),
    )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level.upper())

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger instance."""
    return logging.getLogger(name)
