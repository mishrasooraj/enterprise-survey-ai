from __future__ import annotations

from uuid import UUID

from app.events.event_producer import EventProducer
from app.events.event_schema import EventEnvelope
from app.events.event_schema import EventType
from app.db.models.document import Document
from app.db.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.repositories.document_repository import DocumentRepository
from app.services.chunking_service import DocumentChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import InMemoryVectorStore
from app.services.retrieval_service import RetrievedChunk


class DocumentIngestionService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
        chunking_service: DocumentChunkingService,
        embedding_service: EmbeddingService,
        vector_store: InMemoryVectorStore | None = None,
        event_producer: EventProducer | None = None,
    ):
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store or InMemoryVectorStore()
        self.event_producer = event_producer

    async def ingest_document(
        self,
        *,
        organization_id: UUID,
        title: str,
        content: str,
        metadata: dict | None = None,
        source_name: str | None = None,
        source_type: str | None = None,
    ) -> Document:
        document = await self.document_repository.create(
            Document(
                organization_id=organization_id,
                title=title,
                source_name=source_name,
                source_type=source_type,
                content=content,
                metadata_=metadata,
            )
        )
        if self.event_producer is not None:
            await self.event_producer.publish(
                EventEnvelope(
                    event_type=EventType.document_uploaded,
                    organization_id=organization_id,
                    idempotency_key=f"document-uploaded:{document.id}",
                    payload={
                        "document_id": str(document.id),
                        "title": title,
                        "source_name": source_name,
                        "source_type": source_type,
                    },
                )
            )
        chunks = self.chunking_service.chunk_text(content)
        embeddings = await self.embedding_service.embed_texts(chunks)
        db_chunks = []
        vector_chunks = []
        for index, (chunk_text, embedding) in enumerate(zip(chunks, embeddings, strict=True), start=1):
            db_chunk = DocumentChunk(
                document_id=document.id,
                organization_id=organization_id,
                chunk_index=index,
                content=chunk_text,
                metadata_=metadata,
                embedding_model="hash-embedding" if self.embedding_service.embedding_client is None else "external",
            )
            db_chunks.append(db_chunk)
            vector_chunks.append(
                RetrievedChunk(
                    document_id=str(document.id),
                    chunk_id=str(index),
                    organization_id=str(organization_id),
                    content=chunk_text,
                    embedding=embedding,
                    metadata=metadata,
                )
            )
        await self.chunk_repository.create_many(db_chunks)
        self.vector_store.add(vector_chunks)
        await self.document_repository.db.commit()
        if self.event_producer is not None:
            await self.event_producer.publish(
                EventEnvelope(
                    event_type=EventType.document_processing_completed,
                    organization_id=organization_id,
                    correlation_id=document.id,
                    idempotency_key=f"document-processing-completed:{document.id}",
                    payload={
                        "document_id": str(document.id),
                        "chunk_count": len(db_chunks),
                    },
                )
            )
        return document
