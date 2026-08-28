from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class SurveyStatus(StrEnum):
    draft = "draft"
    active = "active"
    paused = "paused"
    closed = "closed"


class SurveyQuestionCreate(BaseModel):
    question: str = Field(min_length=1, max_length=5000)
    question_type: str = Field(min_length=1, max_length=50)
    options: list[str] | None = None
    order: int = Field(ge=1)
    required: bool = False


class SurveyQuestionRead(SurveyQuestionCreate):
    id: UUID
    survey_id: UUID
    model_config = ConfigDict(from_attributes=True)


class SurveyCreate(BaseModel):
    organization_id: UUID
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: SurveyStatus = SurveyStatus.draft
    questions: list[SurveyQuestionCreate] = Field(default_factory=list)


class SurveyUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: SurveyStatus | None = None
    questions: list[SurveyQuestionCreate] | None = None


class SurveyRead(BaseModel):
    id: UUID
    organization_id: UUID
    title: str
    description: str | None
    status: SurveyStatus
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    questions: list[SurveyQuestionRead] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

