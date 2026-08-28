from uuid import UUID

from app.events.event_producer import EventProducer
from app.events.event_schema import EventEnvelope
from app.events.event_schema import EventType
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.survey import Survey
from app.db.models.survey_question import SurveyQuestion
from app.repositories.survey_repository import SurveyRepository
from app.schemas.survey_generation_schema import SurveyGenerationRequest
from app.services.ai_generation_service import SurveyGenerationService


class SurveyAIWorkflowService:
    def __init__(
        self,
        db: AsyncSession,
        survey_repository: SurveyRepository,
        generation_service: SurveyGenerationService,
        event_producer: EventProducer | None = None,
    ):
        self.db = db
        self.survey_repository = survey_repository
        self.generation_service = generation_service
        self.event_producer = event_producer

    async def generate_and_persist(self, request: SurveyGenerationRequest, created_by: UUID) -> Survey:
        if self.event_producer is not None:
            await self.event_producer.publish(
                EventEnvelope(
                    event_type=EventType.survey_generation_requested,
                    organization_id=request.organization_id,
                    idempotency_key=f"survey-generation-requested:{request.organization_id}:{request.business_requirement}",
                    payload={
                        "business_requirement": request.business_requirement,
                        "desired_question_count": request.desired_question_count,
                        "created_by": str(created_by),
                    },
                )
            )
        draft = await self.generation_service.generate_survey(request)
        survey = await self.survey_repository.create(
            Survey(
                organization_id=request.organization_id,
                title=draft.title,
                description=draft.description,
                status=draft.status,
                created_by=created_by,
                questions=[
                    SurveyQuestion(
                        question=question.question,
                        question_type=question.question_type,
                        options=question.options,
                        order=question.order,
                        required=question.required,
                    )
                    for question in draft.questions
                ],
            )
        )
        await self.db.commit()
        if self.event_producer is not None:
            await self.event_producer.publish(
                EventEnvelope(
                    event_type=EventType.survey_generation_completed,
                    organization_id=request.organization_id,
                    correlation_id=request.organization_id,
                    idempotency_key=f"survey-generation-completed:{survey.id}",
                    payload={
                        "survey_id": str(survey.id),
                        "title": survey.title,
                        "status": survey.status,
                    },
                )
            )
        return survey
