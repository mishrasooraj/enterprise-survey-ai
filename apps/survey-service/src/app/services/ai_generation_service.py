from __future__ import annotations

import inspect
from typing import Any
from uuid import UUID

from app.schemas.survey_generation_schema import GeneratedSurveyDraft
from app.schemas.survey_generation_schema import SurveyGenerationRequest
from app.schemas.survey_generation_schema import SurveyGenerationValidationError
from app.services.prompt_service import SurveyPromptService
from app.services.validation_service import SurveyValidationService


class AIGenerationError(RuntimeError):
    pass


class SurveyGenerationService:
    def __init__(
        self,
        prompt_service: SurveyPromptService | None = None,
        validation_service: SurveyValidationService | None = None,
        llm_client: Any | None = None,
        context_provider: Any | None = None,
    ):
        self.prompt_service = prompt_service or SurveyPromptService()
        self.validation_service = validation_service or SurveyValidationService()
        self.llm_client = llm_client
        self.context_provider = context_provider

    async def retrieve_relevant_enterprise_context(self, request: SurveyGenerationRequest) -> dict[str, str]:
        if self.context_provider is not None:
            context = await self.context_provider(request)
            if isinstance(context, dict):
                return context
            return {"retrieved_context": str(context)}
        return {
            "organization_id": str(request.organization_id),
            "organization_name": request.organization_name,
            "organization_summary": request.organization_summary,
            "target_audience": request.target_audience,
        }

    def _build_deterministic_schema(self, request: SurveyGenerationRequest) -> dict[str, Any]:
        return {
            "title": "",
            "description": None,
            "status": "draft",
            "questions": [],
        }

    async def _call_llm(self, request: SurveyGenerationRequest, context: dict[str, str]) -> dict[str, Any]:
        if self.llm_client is None:
            raise AIGenerationError("LLM client is not configured.")

        system_prompt = self.prompt_service.build_system_prompt()
        user_prompt = self.prompt_service.build_user_prompt(request)

        if hasattr(self.llm_client, "invoke"):
            response = self.llm_client.invoke(
                {
                    "system": system_prompt,
                    "user": user_prompt,
                    "schema": self._build_deterministic_schema(request),
                    "context": context,
                }
            )
        elif callable(self.llm_client):
            response = self.llm_client(system_prompt=system_prompt, user_prompt=user_prompt, context=context)
        else:
            raise AIGenerationError("Unsupported LLM client.")

        if inspect.isawaitable(response):
            response = await response

        if hasattr(response, "model_dump"):
            return response.model_dump()
        if isinstance(response, dict):
            return response
        raise AIGenerationError("LLM client returned unsupported payload.")

    async def generate_survey(self, request: SurveyGenerationRequest) -> GeneratedSurveyDraft:
        context = await self.retrieve_relevant_enterprise_context(request)
        raw = await self._call_llm(request, context)
        try:
            draft = GeneratedSurveyDraft.model_validate(raw)
        except Exception as exc:
            raise SurveyGenerationValidationError(str(exc)) from exc
        return self.validation_service.validate(draft)
