from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_deps import get_db
from app.dependencies.event_dependency import get_event_producer
from app.dependencies.auth_dependency import get_current_user
from app.dependencies.auth_dependency import require_survey_access
from app.events.event_producer import EventProducer
from app.db.models.survey import Survey
from app.repositories.survey_repository import SurveyRepository
from app.schemas.survey_schema import SurveyCreate
from app.schemas.survey_schema import SurveyRead
from app.schemas.survey_schema import SurveyUpdate
from app.services.survey_service import SurveyService


router = APIRouter(prefix="/surveys", tags=["Surveys"])


@router.post("", response_model=SurveyRead, status_code=status.HTTP_201_CREATED)
async def create_survey(
    payload: SurveyCreate,
    current_user: dict = Depends(get_current_user),
    event_producer: EventProducer = Depends(get_event_producer),
    db: AsyncSession = Depends(get_db),
) -> SurveyRead:
    if current_user.get("organization_id") != str(payload.organization_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-tenant access is not allowed.",
        )
    survey = await SurveyService(db=db, survey_repository=SurveyRepository(db)).with_event_producer(event_producer).create_survey(payload, created_by=current_user["sub"])
    return SurveyRead.model_validate(survey)


@router.get("", response_model=list[SurveyRead])
async def list_surveys(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[SurveyRead]:
    surveys = await SurveyService(db=db, survey_repository=SurveyRepository(db)).list_surveys(
        UUID(current_user["organization_id"])
    )
    return [SurveyRead.model_validate(survey) for survey in surveys]


@router.get("/{survey_id}", response_model=SurveyRead)
async def get_survey(
    survey: Survey = Depends(require_survey_access()),
) -> SurveyRead:
    return SurveyRead.model_validate(survey)


@router.patch("/{survey_id}", response_model=SurveyRead)
async def update_survey(
    payload: SurveyUpdate,
    survey: Survey = Depends(require_survey_access()),
    db: AsyncSession = Depends(get_db),
) -> SurveyRead:
    updated = await SurveyService(db=db, survey_repository=SurveyRepository(db)).update_survey(
        survey,
        payload,
    )
    return SurveyRead.model_validate(updated)


@router.delete("/{survey_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_survey(
    survey: Survey = Depends(require_survey_access()),
    db: AsyncSession = Depends(get_db),
) -> None:
    await SurveyService(db=db, survey_repository=SurveyRepository(db)).delete_survey(survey)
