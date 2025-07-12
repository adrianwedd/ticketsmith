from ticketsmith.vector_store import QdrantVectorStore


def ascii_embed(text: str) -> list[float]:
    return [float(ord(text[0])), float(ord(text[-1]))]


def test_qdrant_store_search(tmp_path):
    store = QdrantVectorStore("test", embed_fn=ascii_embed)
    docs = [
        {"text": "hello", "doc_id": "h"},
        {"text": "goodbye", "doc_id": "g"},
    ]
    store.add_documents(docs)

    results = store.similarity_search("hello", top_k=1)
    assert results
    assert results[0]["doc_id"] == "h"
