from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.db.models.document import Document
from app.db.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.repositories.document_repository import DocumentRepository
from app.services.chunking_service import DocumentChunkingService
from app.services.document_ingestion_service import DocumentIngestionService
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import DocumentRetrievalService
from app.services.retrieval_service import InMemoryVectorStore
from app.services.retrieval_service import RetrievedChunk


class FakeDB:
    def __init__(self):
        self.committed = False
        self.flushed = False

    async def commit(self):
        self.committed = True

    async def flush(self):
        self.flushed = True

    async def refresh(self, obj):
        return obj


@pytest.mark.asyncio
async def test_chunking_service_uses_recursive_strategy():
    text = "A" * 2500
    chunks = DocumentChunkingService(chunk_size=1000, chunk_overlap=100).chunk_text(text)
    assert len(chunks) >= 3
    assert chunks[0]


@pytest.mark.asyncio
async def test_embedding_service_hash_fallback_is_deterministic():
    service = EmbeddingService()
    vectors = await service.embed_texts(["hello", "hello"])
    assert vectors[0] == vectors[1]
    assert len(vectors[0]) == 12


@pytest.mark.asyncio
async def test_document_ingestion_persists_and_indexes(monkeypatch):
    db = FakeDB()
    document_repo = DocumentRepository(db)
    chunk_repo = DocumentChunkRepository(db)
    vector_store = InMemoryVectorStore()

    async def fake_create(document):
        document.id = uuid4()
        return document

    async def fake_create_many(chunks):
        for index, chunk in enumerate(chunks, start=1):
            chunk.id = uuid4()
            chunk.document_id = uuid4()
        return chunks

    monkeypatch.setattr(document_repo, "create", fake_create)
    monkeypatch.setattr(chunk_repo, "create_many", fake_create_many)

    service = DocumentIngestionService(
        document_repository=document_repo,
        chunk_repository=chunk_repo,
        chunking_service=DocumentChunkingService(chunk_size=20, chunk_overlap=5),
        embedding_service=EmbeddingService(),
        vector_store=vector_store,
    )

    document = await service.ingest_document(
        organization_id=uuid4(),
        title="Policy",
        content="This is a long policy document. " * 8,
        metadata={"source": "pdf"},
        source_name="policy.pdf",
        source_type="pdf",
    )

    assert document.title == "Policy"
    assert db.committed is True
    assert vector_store._chunks


@pytest.mark.asyncio
async def test_retrieval_filters_by_tenant_and_metadata():
    vector_store = InMemoryVectorStore()
    org_a = str(uuid4())
    org_b = str(uuid4())
    vector_store.add(
        [
            RetrievedChunk(
                document_id=str(uuid4()),
                chunk_id=str(uuid4()),
                organization_id=org_a,
                content="Employee policy context",
                embedding=[1.0, 0.0, 0.0],
                metadata={"source": "pdf", "department": "hr"},
            ),
            RetrievedChunk(
                document_id=str(uuid4()),
                chunk_id=str(uuid4()),
                organization_id=org_b,
                content="Other tenant context",
                embedding=[0.0, 1.0, 0.0],
                metadata={"source": "pdf", "department": "finance"},
            ),
        ]
    )

    results = await DocumentRetrievalService(vector_store=vector_store).retrieve(
        query="employee policy",
        query_embedding=[1.0, 0.0, 0.0],
        organization_id=org_a,
        top_k=5,
        metadata_filter={"source": "pdf"},
    )

    assert len(results) == 1
    assert str(results[0].organization_id) == org_a
