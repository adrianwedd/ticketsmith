from ticketsmith import jira_tools


class DummyJira:
    def __init__(self):
        self.calls = []

    def issue_create(self, fields):
        self.calls.append(("create", fields))
        return {"key": "TST-1"}

    def issue_add_comment(self, key, comment, visibility=None):
        self.calls.append(("comment", key, comment))

    def assign_issue(self, issue, account_id=None):
        self.calls.append(("assign", issue, account_id))

    def get_transition_id_to_status_name(self, key, status_name):
        self.calls.append(("get_transition", key, status_name))
        if status_name == "Done":
            return 31
        return None

    def issue_transition(self, key, status):
        self.calls.append(("transition", key, status))


def test_create_issue(monkeypatch):
    dummy = DummyJira()
    monkeypatch.setattr(jira_tools, "get_jira_client", lambda: dummy)
    result = jira_tools.create_jira_issue(
        project_key="TST", summary="s", description="d", issue_type="Task"
    )
    assert result == "TST-1"
    assert dummy.calls[0][0] == "create"


def test_add_comment(monkeypatch):
    dummy = DummyJira()
    monkeypatch.setattr(jira_tools, "get_jira_client", lambda: dummy)
    jira_tools.add_jira_comment(issue_key="TST-1", comment="hi")
    assert dummy.calls == [("comment", "TST-1", "hi")]


def test_assign_user(monkeypatch):
    dummy = DummyJira()
    monkeypatch.setattr(jira_tools, "get_jira_client", lambda: dummy)
    jira_tools.assign_jira_user(issue_key="TST-1", account_id="acct")
    assert dummy.calls == [("assign", "TST-1", "acct")]


def test_transition(monkeypatch):
    dummy = DummyJira()
    monkeypatch.setattr(jira_tools, "get_jira_client", lambda: dummy)
    jira_tools.transition_jira_issue(issue_key="TST-1", status_name="Done")
    assert ("get_transition", "TST-1", "Done") in dummy.calls and (
        "transition",
        "TST-1",
        "Done",
    ) in dummy.calls


def test_transition_missing(monkeypatch):
    dummy = DummyJira()
    monkeypatch.setattr(jira_tools, "get_jira_client", lambda: dummy)
    try:
        jira_tools.transition_jira_issue(
            issue_key="TST-1",
            status_name="Missing",
        )
    except RuntimeError as e:
        assert "No transition" in str(e)
    else:
        assert False, "expected error"
