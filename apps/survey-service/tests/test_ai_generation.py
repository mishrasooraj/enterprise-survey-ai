from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.schemas.survey_generation_schema import GeneratedSurveyDraft
from app.schemas.survey_generation_schema import SurveyGenerationRequest
from app.schemas.survey_generation_schema import SurveyGenerationValidationError
from app.services.ai_generation_service import SurveyGenerationService
from app.services.survey_generation_service import SurveyAIWorkflowService
from app.services.validation_service import SurveyValidationService


class FakeRepo:
    def __init__(self):
        self.created = []

    async def create(self, survey):
        self.created.append(survey)
        return survey


class FakeDB:
    def __init__(self):
        self.committed = False

    async def commit(self):
        self.committed = True


def build_request() -> SurveyGenerationRequest:
    return SurveyGenerationRequest(
        business_requirement="Measure employee satisfaction across core service teams.",
        organization_id=uuid4(),
        organization_name="Acme Corp",
        organization_summary="Enterprise SaaS organization with distributed product teams.",
        target_audience="Employees across engineering, support, and operations.",
        desired_question_count=5,
        tone="professional",
    )


@pytest.mark.asyncio
async def test_generation_service_returns_validated_draft():
    request = build_request()
    draft = GeneratedSurveyDraft(
        title="Employee Satisfaction Survey",
        description="Measure employee satisfaction across core service teams.",
        status="draft",
        questions=[
            {"question": "How satisfied are you?", "question_type": "rating", "options": None, "order": 1, "required": True},
            {"question": "What could improve?", "question_type": "long_text", "options": None, "order": 2, "required": False},
        ],
    )

    async def fake_context(_request):
        return {"organization_id": str(request.organization_id)}

    async def fake_llm(_request, _context):
        return draft.model_dump()

    service = SurveyGenerationService(llm_client=lambda **kwargs: fake_llm(kwargs.get("request"), kwargs.get("context")))
    service.retrieve_relevant_enterprise_context = fake_context  # type: ignore[method-assign]
    result = await service.generate_survey(request)

    assert result.title == "Employee Satisfaction Survey"
    assert result.questions[0].order == 1


@pytest.mark.asyncio
async def test_generation_service_rejects_invalid_structure():
    request = build_request()

    async def fake_context(_request):
        return {"organization_id": str(request.organization_id)}

    async def fake_llm(_request, _context):
        return {
            "title": "Invalid",
            "description": "",
            "status": "draft",
            "questions": [
                {"question": "Bad type", "question_type": "unsupported", "order": 1, "required": True}
            ],
        }

    service = SurveyGenerationService(llm_client=lambda **kwargs: fake_llm(kwargs.get("request"), kwargs.get("context")))
    service.retrieve_relevant_enterprise_context = fake_context  # type: ignore[method-assign]

    with pytest.raises(SurveyGenerationValidationError):
        await service.generate_survey(request)


@pytest.mark.asyncio
async def test_workflow_persists_generated_survey():
    request = build_request()
    repo = FakeRepo()
    db = FakeDB()

    async def fake_generate_survey(_request):
        return GeneratedSurveyDraft(
            title="Employee Satisfaction Survey",
            description="Measure employee satisfaction.",
            status="draft",
            questions=[
                {"question": "How satisfied are you?", "question_type": "rating", "options": None, "order": 1, "required": True},
            ],
        )

    generation_service = SimpleNamespace(generate_survey=fake_generate_survey)
    workflow = SurveyAIWorkflowService(db=db, survey_repository=repo, generation_service=generation_service)
    survey = await workflow.generate_and_persist(request, created_by=uuid4())

    assert db.committed is True
    assert repo.created
    assert survey.title == "Employee Satisfaction Survey"


def test_validation_rejects_choice_without_options():
    draft = GeneratedSurveyDraft(
        title="Bad Draft",
        description=None,
        status="draft",
        questions=[
            {"question": "Pick one", "question_type": "single_choice", "options": None, "order": 1, "required": True},
        ],
    )

    with pytest.raises(SurveyGenerationValidationError):
        SurveyValidationService().validate(draft)
