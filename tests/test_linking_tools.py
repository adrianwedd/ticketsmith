from ticketsmith import linking_tools


class DummyTools:
    def __init__(self):
        self.calls = []


def test_create_linked(monkeypatch):
    def fake_create_jira_issue(**kwargs):
        dummy.calls.append(("create_issue", kwargs))
        return "TST-1"

    def fake_create_confluence_page(space, title, body):
        dummy.calls.append(("create_page", space, title, body))
        return "42"

    def fake_add_jira_comment(issue_key, comment):
        dummy.calls.append(("comment", issue_key, comment))
        return "ok"

    dummy = DummyTools()
    monkeypatch.setattr(
        linking_tools,
        "create_jira_issue",
        fake_create_jira_issue,
    )
    monkeypatch.setattr(
        linking_tools,
        "create_confluence_page",
        fake_create_confluence_page,
    )
    monkeypatch.setattr(
        linking_tools,
        "add_jira_comment",
        fake_add_jira_comment,
    )
    monkeypatch.setenv("ATLASSIAN_BASE_URL", "https://example.atlassian.net")

    result = linking_tools.create_linked_issue_and_page(
        project_key="TST",
        summary="s",
        description="d",
        issue_type="Task",
        space="DOC",
        title="T",
        body="B",
    )

    assert result == {"issue_key": "TST-1", "page_id": "42"}
    issue_url = "https://example.atlassian.net/browse/TST-1"
    page_url = "https://example.atlassian.net/wiki/spaces/DOC/pages/42"
    assert (
        "create_page",
        "DOC",
        "T",
        "B<p>Related Jira issue: <a href='" + issue_url + "'>TST-1</a></p>",
    ) in dummy.calls
    assert ("comment", "TST-1", f"Confluence page: {page_url}") in dummy.calls
