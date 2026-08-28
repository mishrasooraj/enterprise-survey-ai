from sqlalchemy.ext.asyncio import AsyncSession

from app.events.event_producer import EventProducer
from app.events.event_schema import EventEnvelope
from app.events.event_schema import EventType
from app.db.models.survey import Survey
from app.db.models.survey_question import SurveyQuestion
from app.repositories.survey_repository import SurveyRepository
from app.schemas.survey_schema import SurveyCreate
from app.schemas.survey_schema import SurveyUpdate


class SurveyService:
    def __init__(self, db: AsyncSession, survey_repository: SurveyRepository):
        self.db = db
        self.survey_repository = survey_repository
        self.event_producer: EventProducer | None = None

    def with_event_producer(self, event_producer: EventProducer | None):
        self.event_producer = event_producer
        return self

    async def create_survey(self, payload: SurveyCreate, created_by: str) -> Survey:
        survey = await self.survey_repository.create(
            Survey(
                organization_id=payload.organization_id,
                title=payload.title,
                description=payload.description,
                status=payload.status.value,
                created_by=created_by,
                questions=[
                    SurveyQuestion(
                        question=q.question,
                        question_type=q.question_type,
                        options=q.options,
                        order=q.order,
                        required=q.required,
                    )
                    for q in payload.questions
                ],
            )
        )
        await self.db.commit()
        if self.event_producer is not None:
            await self.event_producer.publish(
                EventEnvelope(
                    event_type=EventType.survey_created,
                    organization_id=payload.organization_id,
                    idempotency_key=f"survey-created:{survey.id}",
                    payload={
                        "survey_id": str(survey.id),
                        "title": survey.title,
                        "status": survey.status,
                        "created_by": str(created_by),
                    },
                )
            )
        return survey

    async def list_surveys(self, organization_id):
        return await self.survey_repository.list_by_organization(organization_id)

    async def get_survey(self, survey):
        return survey

    async def update_survey(self, survey: Survey, payload: SurveyUpdate) -> Survey:
        if payload.title is not None:
            survey.title = payload.title
        if payload.description is not None:
            survey.description = payload.description
        if payload.status is not None:
            survey.status = payload.status.value
        if payload.questions is not None:
            survey.questions = [
                SurveyQuestion(
                    question=q.question,
                    question_type=q.question_type,
                    options=q.options,
                    order=q.order,
                    required=q.required,
                )
                for q in payload.questions
            ]
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(survey)
        return survey

    async def delete_survey(self, survey: Survey) -> None:
        await self.survey_repository.delete(survey)
        await self.db.commit()
