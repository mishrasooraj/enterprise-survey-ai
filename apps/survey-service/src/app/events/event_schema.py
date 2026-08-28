from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class EventType(StrEnum):
    survey_created = "survey.created"
    survey_generation_requested = "survey.generation.requested"
    survey_generation_completed = "survey.generation.completed"
    document_uploaded = "document.uploaded"
    document_processing_completed = "document.processing.completed"


class EventEnvelope(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: EventType
    organization_id: UUID
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: UUID | None = None
    idempotency_key: str
    payload: dict
    model_config = ConfigDict(extra="forbid")

