from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.document import Document


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, document: Document) -> Document:
        self.db.add(document)
        await self.db.flush()
        await self.db.refresh(document)
        return document

    async def get_by_id(self, document_id: UUID) -> Document | None:
        result = await self.db.execute(
            select(Document)
            .options(selectinload(Document.chunks))
            .where(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def list_by_organization(self, organization_id: UUID) -> list[Document]:
        result = await self.db.execute(
            select(Document)
            .options(selectinload(Document.chunks))
            .where(Document.organization_id == organization_id)
            .order_by(Document.created_at.desc())
        )
        return list(result.scalars().all())

