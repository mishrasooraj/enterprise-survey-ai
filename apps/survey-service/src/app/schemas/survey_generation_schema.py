from __future__ import annotations

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class SurveyGenerationRequest(BaseModel):
    business_requirement: str = Field(min_length=10, max_length=4000)
    organization_id: UUID
    organization_name: str = Field(min_length=1, max_length=255)
    organization_summary: str = Field(default="", max_length=6000)
    target_audience: str = Field(default="", max_length=2000)
    desired_question_count: int = Field(default=8, ge=3, le=25)
    tone: str = Field(default="professional", max_length=100)


class SurveyQuestionDraft(BaseModel):
    question: str = Field(min_length=1, max_length=5000)
    question_type: str = Field(min_length=1, max_length=50)
    options: list[str] | None = None
    order: int = Field(ge=1)
    required: bool = False
    model_config = ConfigDict(extra="forbid")


class GeneratedSurveyDraft(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: str = "draft"
    questions: list[SurveyQuestionDraft] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class SurveyGenerationValidationError(ValueError):
    pass

