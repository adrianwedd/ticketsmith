"""Audit logging utilities."""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Any

import structlog

# Security-relevant events that should be audited
SECURITY_EVENTS = {
    "login",
    "data_access",
    "permission_change",
    "token_validated",
    "token_invalid",
    "insufficient_scope",
}


class AppendOnlyRotatingFileHandler(RotatingFileHandler):
    """Rotating file handler that opens files in append-only mode."""

    def _open(self):  # type: ignore[override]
        flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
        fd = os.open(self.baseFilename, flags, 0o600)
        return open(fd, self.mode, encoding=self.encoding)


def configure_audit_logging(
    path: str | None = None, max_bytes: int = 1_000_000, backup_count: int = 30
) -> None:
    """Configure the dedicated audit logger.

    Args:
        path: Optional path to the audit log file.
        max_bytes: Maximum log file size before rotation.
        backup_count: Number of rotated files to retain.
    """
    log_path = path or os.getenv("AUDIT_LOG_PATH", "audit.log")
    handler = AppendOnlyRotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger = logging.getLogger("audit")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False


_logger = structlog.get_logger("audit")


def log_security_event(event: str, user: str, **details: Any) -> None:
    """Emit an audit log entry for the given security event."""
    if event not in SECURITY_EVENTS:
        raise ValueError(f"Unknown security event: {event}")
    _logger.info(event, user=user, **details)
