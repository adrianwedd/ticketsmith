import os
import sys
import json
import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


@pytest.fixture(autouse=True)
def scoped_token(monkeypatch):
    """Provide a default scoped token for tool API tests."""
    scopes = {
        "test-token": [
            "misc:echo",
            "math:add",
            "jira:issue:create",
            "jira:comment:add",
            "jira:issue:assign",
            "jira:issue:transition",
            "confluence:page:create",
            "confluence:page:read",
            "confluence:page:update",
            "kb:read",
            "link:create",
        ]
    }
    monkeypatch.setenv("TOOL_TOKENS", json.dumps(scopes))
    monkeypatch.setenv("TOOL_ACCESS_TOKEN", "test-token")
