from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any

from app.schemas.document_schema import RetrievedContextItem


@dataclass(slots=True)
class RetrievedChunk:
    document_id: str
    chunk_id: str
    organization_id: str
    content: str
    embedding: list[float]
    metadata: dict | None = None
    score: float | None = None


class InMemoryVectorStore:
    def __init__(self):
        self._chunks: list[RetrievedChunk] = []

    def add(self, chunks: list[RetrievedChunk]) -> None:
        self._chunks.extend(chunks)

    def search(self, query_embedding: list[float], organization_id: str, top_k: int = 5) -> list[RetrievedChunk]:
        candidates = [chunk for chunk in self._chunks if chunk.organization_id == organization_id]
        scored = [
            RetrievedChunk(
                document_id=chunk.document_id,
                chunk_id=chunk.chunk_id,
                organization_id=chunk.organization_id,
                content=chunk.content,
                embedding=chunk.embedding,
                metadata=chunk.metadata,
                score=self._cosine_similarity(query_embedding, chunk.embedding),
            )
            for chunk in candidates
        ]
        scored.sort(key=lambda item: item.score or 0.0, reverse=True)
        return scored[:top_k]

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        dot = sum(a * b for a, b in zip(left, right))
        left_norm = sqrt(sum(a * a for a in left)) or 1.0
        right_norm = sqrt(sum(b * b for b in right)) or 1.0
        return dot / (left_norm * right_norm)


class DocumentRetrievalService:
    def __init__(self, vector_store: Any | None = None, reranker: Any | None = None):
        self.vector_store = vector_store or InMemoryVectorStore()
        self.reranker = reranker

    async def retrieve(
        self,
        query: str,
        query_embedding: list[float],
        organization_id: str,
        top_k: int = 5,
        metadata_filter: dict | None = None,
    ) -> list[RetrievedContextItem]:
        candidates = self.vector_store.search(query_embedding=query_embedding, organization_id=organization_id, top_k=top_k)
        if metadata_filter:
            candidates = [
                chunk
                for chunk in candidates
                if not chunk.metadata or all(chunk.metadata.get(key) == value for key, value in metadata_filter.items())
            ]
        if self.reranker is not None:
            candidates = self.reranker.rerank(query, candidates)
        return [
            RetrievedContextItem(
                document_id=chunk.document_id,
                chunk_id=chunk.chunk_id,
                organization_id=chunk.organization_id,
                content=chunk.content,
                score=chunk.score,
                metadata=chunk.metadata,
            )
            for chunk in candidates
        ]
