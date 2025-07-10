from __future__ import annotations

import json
import os
import re
from typing import Any, Callable, Dict, Iterable, List


class ConversationBuffer:
    """Maintain a sliding window of recent conversation steps."""

    def __init__(self, window_size: int = 10) -> None:
        self.window_size = window_size
        self._history: List[Dict[str, Any]] = []

    def add(self, step: Dict[str, Any]) -> None:
        """Add a step to the buffer, trimming if necessary."""
        self._history.append(step)
        if len(self._history) > self.window_size:
            self._history.pop(0)

    def get_history(self) -> List[Dict[str, Any]]:
        """Return the current conversation history."""
        return list(self._history)

    def clear(self) -> None:
        """Remove all stored steps."""
        self._history.clear()


TokenList = List[str]


def default_embed(text: str) -> TokenList:
    """Simple embedding function returning lowercase word tokens."""
    return re.findall(r"[\w']+", text.lower())


def jaccard_similarity(a: Iterable[str], b: Iterable[str]) -> float:
    """Compute Jaccard similarity between two token sets."""
    set_a, set_b = set(a), set(b)
    if not set_a and not set_b:
        return 1.0
    return len(set_a & set_b) / float(len(set_a | set_b))


class SimpleVectorStore:
    """Minimal persistent vector store using token-based embeddings."""

    def __init__(
        self,
        store_path: str,
        embed_fn: Callable[[str], TokenList] | None = None,
    ) -> None:
        self.store_path = store_path
        self.embed_fn = embed_fn or default_embed
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.store_path):
            with open(self.store_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data: List[Dict[str, Any]] = []

    def _save(self) -> None:
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f)

    def add(self, text: str) -> None:
        """Add a text entry to the store."""
        embedding = self.embed_fn(text)
        self._data.append({"text": text, "embedding": embedding})
        self._save()

    def similarity_search(
        self,
        query: str,
        top_k: int = 1,
    ) -> List[Dict[str, Any]]:
        """Return entries most similar to the query."""
        query_emb = self.embed_fn(query)
        scored = [
            (jaccard_similarity(query_emb, item["embedding"]), item)
            for item in self._data
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _score, item in scored[:top_k]]
