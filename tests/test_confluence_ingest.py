from ticketsmith.confluence_ingest import ConfluenceIngestor


class DummyConfluence:
    def __init__(self, body="<p>Hello</p>", version=1):
        self.body = body
        self.version = version
        self.calls = []

    def get_page_by_id(self, page_id, expand=None):
        self.calls.append((page_id, expand))
        return {
            "body": {"storage": {"value": self.body}},
            "version": {"number": self.version},
        }


def test_sync_new_page(tmp_path, monkeypatch):
    dummy = DummyConfluence()
    monkeypatch.setattr(
        "ticketsmith.confluence_ingest.get_confluence_client", lambda: dummy
    )
    monkeypatch.setattr(
        "ticketsmith.confluence_ingest.search_confluence",
        lambda q: {"results": [{"content": {"id": "1"}}]},
    )
    ing = ConfluenceIngestor(str(tmp_path / "index.json"))
    chunks = ing.sync("query")
    assert chunks[0]["text"] == "Hello"
    assert dummy.calls


def test_sync_delete(tmp_path, monkeypatch):
    dummy = DummyConfluence()
    monkeypatch.setattr(
        "ticketsmith.confluence_ingest.get_confluence_client", lambda: dummy
    )
    results = {"results": [{"content": {"id": "1"}}]}
    monkeypatch.setattr(
        "ticketsmith.confluence_ingest.search_confluence", lambda q: results
    )
    ing = ConfluenceIngestor(str(tmp_path / "index.json"))
    ing.sync("query")
    results["results"] = []
    chunks = ing.sync("query")
    assert chunks == []
