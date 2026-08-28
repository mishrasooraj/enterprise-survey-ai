from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.role import Role


class RoleRepository:
    """
    Repository for role database operations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        role: Role,
    ) -> Role:
        """
        Create a new role.
        """

        self.db.add(role)
        await self.db.flush()
        await self.db.refresh(role)

        return role

    async def get_by_name(
        self,
        organization_id: UUID,
        name: str,
    ) -> Role | None:
        """
        Get a role by name within an organization.
        """

        result = await self.db.execute(
            select(Role).where(
                Role.organization_id == organization_id,
                Role.name == name,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        role_id: UUID,
    ) -> Role | None:
        """
        Get a role by ID.
        """

        result = await self.db.execute(
            select(Role).where(
                Role.id == role_id,
            )
        )

        return result.scalar_one_or_none()

    async def create_default_roles(
        self,
        organization_id: UUID,
    ) -> list[Role]:
        """
        Create the default roles for a new organization.
        """

        roles = [
            Role(
                name="Admin",
                organization_id=organization_id,
            ),
            Role(
                name="Manager",
                organization_id=organization_id,
            ),
            Role(
                name="Employee",
                organization_id=organization_id,
            ),
        ]

        self.db.add_all(roles)

        await self.db.flush()

        for role in roles:
            await self.db.refresh(role)

        return roles
