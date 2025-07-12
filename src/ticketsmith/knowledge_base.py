from __future__ import annotations

from typing import Any, Dict, List

from .vector_store import QdrantVectorStore
from .tools import tool


# Default collection name for Qdrant
_DEFAULT_COLLECTION = "ticketsmith_docs"
# The global vector store instance can be patched in tests
vector_store = QdrantVectorStore(_DEFAULT_COLLECTION)


def retrieve_relevant_chunks(query: str, top_k: int = 5) -> str:
    """Return relevant knowledge base chunks for ``query``.

    Args:
        query: Natural language query string.
        top_k: Number of similar chunks to retrieve.

    Returns:
        Formatted string with chunk text and metadata.
    """
    results: List[Dict[str, Any]] = vector_store.similarity_search(
        query,
        top_k=top_k,
    )
    lines = []
    for res in results:
        meta = {k: v for k, v in res.items() if k not in {"text", "score"}}
        meta_str = ", ".join(f"{k}={v}" for k, v in meta.items())
        line = res.get("text", "")
        if meta_str:
            line = f"[{meta_str}] {line}"
        lines.append(line)
    return "\n".join(lines)


@tool(
    name="knowledge_base_search",
    description=(
        "Search the internal knowledge base for relevant document chunks"
        " and return them formatted for prompting."
    ),
)
def knowledge_base_search(query: str) -> str:
    """LangChain tool wrapper for :func:`retrieve_relevant_chunks`."""
    return retrieve_relevant_chunks(query)
