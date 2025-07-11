"""Utilities for ingesting Confluence pages into text chunks."""

from __future__ import annotations

import json
import os
from typing import Dict, List

from bs4 import BeautifulSoup

from .atlassian_auth import get_confluence_client
from .confluence_tools import search_confluence


def extract_text(html: str) -> str:
    """Return plain text from Confluence storage format."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def chunk_text(text: str, size: int = 1000, overlap: int = 200) -> List[str]:
    """Split ``text`` into overlapping chunks."""
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


class ConfluenceIngestor:
    """Fetch pages from Confluence and maintain a local index."""

    def __init__(self, index_path: str) -> None:
        self.index_path = index_path
        self._load()
        self.client = get_confluence_client()

    def _load(self) -> None:
        if os.path.exists(self.index_path):
            with open(self.index_path, "r", encoding="utf-8") as f:
                self.index: Dict[str, Dict[str, object]] = json.load(f)
        else:
            self.index = {}

    def _save(self) -> None:
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.index, f)

    def sync(self, query: str) -> List[Dict[str, object]]:
        """Fetch updated pages matching ``query`` and update the index."""
        results = search_confluence(query).get("results", [])
        seen: set[str] = set()
        for res in results:
            page_id = str(res.get("id") or res.get("content", {}).get("id"))
            if not page_id:
                continue
            seen.add(page_id)
            page = self.client.get_page_by_id(
                page_id,
                expand="body.storage,version",
            )
            version = page.get("version", {}).get("number", 0)
            stored = self.index.get(page_id, {})
            if stored.get("version") == version:
                continue
            text = extract_text(
                page.get("body", {}).get("storage", {}).get("value", "")
            )
            chunks = chunk_text(text)
            self.index[page_id] = {"version": version, "chunks": chunks}
        for pid in list(self.index):
            if pid not in seen:
                del self.index[pid]
        self._save()
        all_chunks = []
        for pid, data in self.index.items():
            for i, chunk in enumerate(data["chunks"]):
                all_chunks.append(
                    {
                        "page_id": pid,
                        "version": data["version"],
                        "index": i,
                        "text": chunk,
                    }
                )
        return all_chunks
