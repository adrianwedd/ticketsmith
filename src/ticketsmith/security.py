"""Security utilities for input sanitization and validation."""

from __future__ import annotations

import ast
import re
from typing import Any, Dict

import scrubadub


SUSPICIOUS_PATTERNS = [
    re.compile(r"shutdown", re.IGNORECASE),
    re.compile(r"rm\s+-rf", re.IGNORECASE),
    re.compile(r"drop\s+table", re.IGNORECASE),
]

scrubber = scrubadub.Scrubber()


def sanitize_input(text: str) -> str:
    """Sanitize user input by redacting suspicious patterns and PII.

    Args:
        text: Raw user provided text.

    Returns:
        The sanitized text with dangerous patterns and PII replaced by
        placeholders.
    """
    for pattern in SUSPICIOUS_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    text = scrubber.clean(text)
    return text


def redact_pii(obj: Any) -> Any:
    """Recursively redact PII from the given object."""
    if isinstance(obj, str):
        return scrubber.clean(obj)
    if isinstance(obj, dict):
        return {key: redact_pii(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [redact_pii(item) for item in obj]
    return obj


class GuardrailModel:
    """Simple guardrail model that flags suspicious prompts."""

    def check(self, text: str) -> bool:
        """Return True if the text passes the guardrail check."""
        for pattern in SUSPICIOUS_PATTERNS:
            if pattern.search(text):
                return False
        return True


def parse_args(arg_str: str) -> Dict[str, Any]:
    """Safely parse tool arguments from a string."""
    if not arg_str:
        return {}
    try:
        items = []
        for part in arg_str.split(","):
            key, value = part.split("=", 1)
            items.append((key.strip(), ast.literal_eval(value.strip())))
        parsed = {k: v for k, v in items}
    except (SyntaxError, ValueError) as exc:
        raise ValueError(f"Failed to parse arguments: {exc}") from exc
    return validate_tool_args(parsed)


def validate_tool_args(args: Dict[str, Any]) -> Dict[str, Any]:
    """Validate that tool arguments contain only simple builtin types."""
    for key, value in args.items():
        if not isinstance(value, (str, int, float, bool)):
            raise ValueError(f"Invalid argument {key}: {type(value)}")
    return args
