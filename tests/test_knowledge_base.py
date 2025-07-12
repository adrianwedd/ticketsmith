from ticketsmith.vector_store import QdrantVectorStore
from ticketsmith import knowledge_base_search, retrieve_relevant_chunks
import ticketsmith.knowledge_base as kb


def ascii_embed(text: str) -> list[float]:
    return [float(ord(text[0])), float(ord(text[-1]))]


def test_retrieve_relevant_chunks(monkeypatch):
    store = QdrantVectorStore("test", embed_fn=ascii_embed)
    store.add_documents(
        [
            {"text": "hello world", "page_id": "1", "index": 0},
            {"text": "goodbye", "page_id": "2", "index": 0},
        ]
    )
    monkeypatch.setattr(kb, "vector_store", store)
    output = retrieve_relevant_chunks("hello")
    assert "hello world" in output
    assert "page_id=1" in output


def test_tool_wrapper(monkeypatch):
    store = QdrantVectorStore("test2", embed_fn=ascii_embed)
    store.add_documents([{"text": "alpha", "page_id": "a", "index": 0}])
    monkeypatch.setattr(kb, "vector_store", store)
    result = knowledge_base_search(query="alpha")
    assert "alpha" in result
