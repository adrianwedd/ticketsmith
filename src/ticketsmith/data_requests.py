"""Utilities for GDPR data deletion and export requests."""

from __future__ import annotations

import shutil
from pathlib import Path

from .audit import log_security_event


def delete_user_data(user_id: str, path: str) -> None:
    """Delete a user's data file and log the action.

    Args:
        user_id: Identifier for the user.
        path: File path containing the user's data.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(path)
    file_path.unlink()
    log_security_event("data_deletion", user=user_id, path=str(file_path))


def export_user_data(user_id: str, source: str, destination: str) -> None:
    """Export user data to ``destination`` and log the action.

    Args:
        user_id: Identifier for the user.
        source: Path to the source data file.
        destination: Location to copy the data.
    """
    src = Path(source)
    dest = Path(destination)
    if not src.exists():
        raise FileNotFoundError(source)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    log_security_event(
        "data_export", user=user_id, source=str(src), destination=str(dest)
    )
