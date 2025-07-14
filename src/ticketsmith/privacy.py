"""Utilities for the processing register and DPIA records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _load(path: Path) -> list[dict[str, Any]]:
    if path.exists():
        return json.loads(path.read_text())
    return []


def _save(path: Path, data: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(data, indent=2))


def add_processing_activity(path: str, activity: dict[str, Any]) -> None:
    """Append a processing activity to the register at ``path``.

    Args:
        path: File path to the JSON register.
        activity: Mapping describing the processing activity.
    """
    register = _load(Path(path))
    register.append(activity)
    _save(Path(path), register)


def record_dpia(
    path: str,
    feature: str,
    risks: list[str],
    mitigations: str,
) -> None:
    """Record a Data Protection Impact Assessment.

    Args:
        path: Location of the DPIA register JSON file.
        feature: Name of the assessed feature.
        risks: List of identified risks.
        mitigations: Summary of mitigation measures.
    """
    record = {"feature": feature, "risks": risks, "mitigations": mitigations}
    register = _load(Path(path))
    register.append(record)
    _save(Path(path), register)
