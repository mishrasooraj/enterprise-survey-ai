from __future__ import annotations

import hashlib
from typing import Any


class EmbeddingService:
    def __init__(self, embedding_client: Any | None = None):
        self.embedding_client = embedding_client

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if self.embedding_client is None:
            return [self._hash_embed(text) for text in texts]

        if hasattr(self.embedding_client, "embed_documents"):
            vectors = self.embedding_client.embed_documents(texts)
        elif hasattr(self.embedding_client, "aembed_documents"):
            vectors = await self.embedding_client.aembed_documents(texts)
        elif callable(self.embedding_client):
            vectors = self.embedding_client(texts)
        else:
            raise RuntimeError("Unsupported embedding client.")

        return vectors

    def _hash_embed(self, text: str, dimensions: int = 12) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values: list[float] = []
        for index in range(dimensions):
            byte = digest[index % len(digest)]
            values.append(round(byte / 255.0, 6))
        return values

