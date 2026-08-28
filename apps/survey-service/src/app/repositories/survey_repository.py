from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.survey import Survey


class SurveyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, survey: Survey) -> Survey:
        self.db.add(survey)
        await self.db.flush()
        await self.db.refresh(survey)
        return survey

    async def get_by_id(self, survey_id: UUID) -> Survey | None:
        result = await self.db.execute(
            select(Survey)
            .options(selectinload(Survey.questions))
            .where(Survey.id == survey_id)
        )
        return result.scalar_one_or_none()

    async def list_by_organization(self, organization_id: UUID) -> list[Survey]:
        result = await self.db.execute(
            select(Survey)
            .options(selectinload(Survey.questions))
            .where(Survey.organization_id == organization_id)
            .order_by(Survey.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete(self, survey: Survey) -> None:
        await self.db.delete(survey)

