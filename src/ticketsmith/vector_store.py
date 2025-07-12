from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - optional dependency
    SentenceTransformer = None  # type: ignore


EmbedFn = Callable[[str], List[float]]


class QdrantVectorStore:
    """Store and query embeddings using Qdrant."""

    def __init__(
        self,
        collection_name: str,
        client: Optional[QdrantClient] = None,
        embed_fn: Optional[EmbedFn] = None,
    ) -> None:
        self.collection_name = collection_name
        self.client = client or QdrantClient(path=":memory:")
        self.embed_fn = embed_fn or self._default_embed
        self._collection_initialized = False
        self._next_id = 0

    def _default_embed(self, text: str) -> List[float]:
        if SentenceTransformer is None:
            raise RuntimeError(
                "sentence-transformers is required for default embeddings"
            )
        if not hasattr(self, "_model"):
            self._model = SentenceTransformer("nomic-ai/nomic-embed-text-v1")
        vector = self._model.encode(text)
        return vector.tolist()

    def _ensure_collection(self, vector_size: int) -> None:
        if self._collection_initialized:
            return
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=rest.VectorParams(
                size=vector_size, distance=rest.Distance.COSINE
            ),
        )
        self._collection_initialized = True

    def add_documents(self, docs: Iterable[Dict[str, Any]]) -> None:
        docs_list = list(docs)
        if not docs_list:
            return
        vectors = [self.embed_fn(d["text"]) for d in docs_list]
        self._ensure_collection(len(vectors[0]))
        payloads = []
        for doc in docs_list:
            payloads.append({k: v for k, v in doc.items() if k != "text"})
        points = [
            rest.PointStruct(id=self._next_id + i, vector=vec, payload=pl)
            for i, (vec, pl) in enumerate(zip(vectors, payloads))
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)
        self._next_id += len(points)

    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        if not self._collection_initialized:
            return []
        vector = self.embed_fn(query)
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=top_k,
        )
        return [{"score": res.score, **(res.payload or {})} for res in results]
