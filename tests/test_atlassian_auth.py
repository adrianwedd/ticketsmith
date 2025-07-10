import os

import pytest

from ticketsmith import atlassian_auth


class Dummy:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


def test_get_jira_client(monkeypatch):
    monkeypatch.setitem(
        os.environ, "ATLASSIAN_BASE_URL", "https://example.atlassian.net"
    )
    monkeypatch.setitem(os.environ, "ATLASSIAN_USERNAME", "user")
    monkeypatch.setitem(os.environ, "ATLASSIAN_API_TOKEN", "token")

    called = {}

    def fake_jira(url, username, password):
        called.update(url=url, username=username, password=password)
        return Dummy(url=url, username=username, password=password)

    monkeypatch.setattr(atlassian_auth, "Jira", fake_jira)

    client = atlassian_auth.get_jira_client()
    assert isinstance(client, Dummy)
    assert called == {
        "url": "https://example.atlassian.net",
        "username": "user",
        "password": "token",
    }


def test_missing_env(monkeypatch):
    monkeypatch.delenv("ATLASSIAN_BASE_URL", raising=False)
    with pytest.raises(atlassian_auth.AtlassianAuthError):
        atlassian_auth.get_jira_client()
