from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document_chunk import DocumentChunk


class DocumentChunkRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(self, chunks: list[DocumentChunk]) -> list[DocumentChunk]:
        self.db.add_all(chunks)
        await self.db.flush()
        for chunk in chunks:
            await self.db.refresh(chunk)
        return chunks

    async def list_by_document(self, document_id: UUID) -> list[DocumentChunk]:
        result = await self.db.execute(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index.asc())
        )
        return list(result.scalars().all())

