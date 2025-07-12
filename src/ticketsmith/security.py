"""Security utilities for input sanitization and validation."""

from __future__ import annotations

import ast
import re
from typing import Any, Dict


SUSPICIOUS_PATTERNS = [
    re.compile(r"shutdown", re.IGNORECASE),
    re.compile(r"rm\s+-rf", re.IGNORECASE),
    re.compile(r"drop\s+table", re.IGNORECASE),
]


def sanitize_input(text: str) -> str:
    """Sanitize user input by redacting suspicious patterns.

    Args:
        text: Raw user provided text.

    Returns:
        The sanitized text with dangerous patterns replaced by '[REDACTED]'.
    """
    for pattern in SUSPICIOUS_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


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
        parsed = ast.literal_eval(f"dict({arg_str})")
    except (SyntaxError, ValueError) as exc:
        raise ValueError(f"Failed to parse arguments: {exc}") from exc
    return validate_tool_args(parsed)


def validate_tool_args(args: Dict[str, Any]) -> Dict[str, Any]:
    """Validate that tool arguments contain only simple builtin types."""
    for key, value in args.items():
        if not isinstance(value, (str, int, float, bool)):
            raise ValueError(f"Invalid argument {key}: {type(value)}")
    return args
