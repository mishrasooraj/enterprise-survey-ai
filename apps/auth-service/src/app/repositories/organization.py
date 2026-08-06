from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.organization import Organization


class OrganizationRepository:
    """
    Repository for organization database operations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        organization: Organization,
    ) -> Organization:
        """
        Create a new organization.
        """

        self.db.add(organization)

        await self.db.flush()
        await self.db.refresh(organization)

        return organization

    async def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        """
        Get organization by slug.
        """

        result = await self.db.execute(
            select(Organization).where(
                Organization.slug == slug,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        """
        Get organization by ID.
        """

        result = await self.db.execute(
            select(Organization).where(
                Organization.id == organization_id,
            )
        )

        return result.scalar_one_or_none()
