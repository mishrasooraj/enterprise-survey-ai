from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.models.model_base import BaseModel


class DocumentChunk(BaseModel):
    __tablename__ = "document_chunks"

    document_id: Mapped[UUID] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)
    embedding_model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    vector_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    document: Mapped["Document"] = relationship(back_populates="chunks", lazy="selectin")
