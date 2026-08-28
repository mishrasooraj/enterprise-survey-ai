from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class DocumentChunkRead(BaseModel):
    id: UUID
    document_id: UUID
    organization_id: UUID
    chunk_index: int
    content: str
    metadata: dict | None = None
    embedding_model: str | None = None
    vector_id: str | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DocumentCreate(BaseModel):
    organization_id: UUID
    title: str = Field(min_length=1, max_length=255)
    source_name: str | None = Field(default=None, max_length=255)
    source_type: str | None = Field(default=None, max_length=100)
    content: str = Field(min_length=1, max_length=200000)
    metadata: dict | None = None


class DocumentRead(BaseModel):
    id: UUID
    organization_id: UUID
    title: str
    source_name: str | None = None
    source_type: str | None = None
    content: str
    metadata: dict | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    chunks: list[DocumentChunkRead] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class ChunkRequest(BaseModel):
    content: str = Field(min_length=1)
    chunk_size: int = Field(default=1000, ge=100, le=4000)
    chunk_overlap: int = Field(default=150, ge=0, le=1000)


class RetrievedContextItem(BaseModel):
    document_id: UUID
    chunk_id: UUID
    organization_id: UUID
    content: str
    score: float | None = None
    metadata: dict | None = None
    model_config = ConfigDict(from_attributes=True)

