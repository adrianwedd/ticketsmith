"""Token validation helpers for tool access."""

from __future__ import annotations

import json
import os
from typing import Dict, Set

from .audit import log_security_event


class InvalidTokenError(PermissionError):
    """Raised when an access token is missing or invalid."""


class InsufficientScopeError(PermissionError):
    """Raised when the token lacks the required scope."""


def load_token_scopes() -> Dict[str, Set[str]]:
    """Load token->scopes mapping from ``TOOL_TOKENS`` env var."""
    data = os.getenv("TOOL_TOKENS", "{}")
    try:
        raw: Dict[str, list[str]] = json.loads(data)
    except json.JSONDecodeError as exc:
        raise RuntimeError("TOOL_TOKENS must be JSON") from exc
    return {token: set(scopes) for token, scopes in raw.items()}


def validate_token(
    token: str, scope: str, token_scopes: Dict[str, Set[str]] | None = None
) -> None:
    """Validate that ``token`` exists and grants ``scope``."""
    if token_scopes is None:
        token_scopes = load_token_scopes()
    scopes = token_scopes.get(token)
    if scopes is None:
        log_security_event("token_invalid", user=token)
        raise InvalidTokenError("401 Unauthorized: invalid token")
    if scope not in scopes:
        log_security_event("insufficient_scope", user=token, scope=scope)
        raise InsufficientScopeError("403 Forbidden: insufficient scope")
    log_security_event("token_validated", user=token, scope=scope)
