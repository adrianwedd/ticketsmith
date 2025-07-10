from ticketsmith import confluence_tools


class DummyConfluence:
    def __init__(self):
        self.calls = []

    def create_page(self, space, title, body):
        self.calls.append(("create", space, title, body))
        return {"id": "42"}

    def cql(self, query):
        self.calls.append(("search", query))
        return {"results": [1]}

    def append_page(self, page_id, content):
        self.calls.append(("append", page_id, content))


def test_create_page(monkeypatch):
    dummy = DummyConfluence()
    monkeypatch.setattr(confluence_tools, "get_confluence_client", lambda: dummy)
    result = confluence_tools.create_confluence_page(
        space="TS", title="Title", body="Body"
    )
    assert result == "42"
    assert dummy.calls == [("create", "TS", "Title", "Body")]


def test_search(monkeypatch):
    dummy = DummyConfluence()
    monkeypatch.setattr(confluence_tools, "get_confluence_client", lambda: dummy)
    result = confluence_tools.search_confluence(query="hello")
    assert result == {"results": [1]}
    assert dummy.calls == [("search", "siteSearch ~ 'hello'")]


def test_append_page(monkeypatch):
    dummy = DummyConfluence()
    monkeypatch.setattr(confluence_tools, "get_confluence_client", lambda: dummy)
    msg = confluence_tools.append_to_confluence_page(page_id="1", content="content")
    assert msg == "content appended"
    assert dummy.calls == [("append", "1", "content")]
