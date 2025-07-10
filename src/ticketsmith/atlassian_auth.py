from __future__ import annotations

import os

from atlassian import Confluence, Jira


class AtlassianAuthError(RuntimeError):
    """Raised when required authentication variables are missing."""


def _get_env(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError as exc:
        msg = f"Environment variable '{name}' is required"
        raise AtlassianAuthError(msg) from exc


def get_jira_client() -> Jira:
    """Return an authenticated Jira client using environment variables."""
    base_url = _get_env("ATLASSIAN_BASE_URL")
    username = _get_env("ATLASSIAN_USERNAME")
    token = _get_env("ATLASSIAN_API_TOKEN")
    return Jira(url=base_url, username=username, password=token)


def get_confluence_client() -> Confluence:
    """Return an authenticated Confluence client using env vars."""
    base_url = _get_env("ATLASSIAN_BASE_URL")
    username = _get_env("ATLASSIAN_USERNAME")
    token = _get_env("ATLASSIAN_API_TOKEN")
    return Confluence(url=base_url, username=username, password=token)


def get_clients() -> tuple[Jira, Confluence]:
    """Return both Jira and Confluence clients."""
    return get_jira_client(), get_confluence_client()
