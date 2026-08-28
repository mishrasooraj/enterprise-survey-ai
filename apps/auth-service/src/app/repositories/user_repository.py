from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserRepository:
    """
    Repository responsible for all database operations
    related to the User model.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """
        Retrieve a user by ID.

        Returns:
            User if found, otherwise None.
        """
        statement = (
            select(User)
            .where(User.id == user_id)
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.

        Returns:
            User if found, otherwise None.
        """
        statement = (
            select(User)
            .where(User.email == email)
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def create(
        self,
        user: User,
    ) -> User:
        """
        Create a new user.
        """
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)

        return user

    async def update(
        self,
        user: User,
    ) -> User:
        """
        Persist changes made to an existing user.
        """
        await self.db.refresh(user)

        return user

    async def delete(
        self,
        user: User,
    ) -> None:
        """
        Delete a user from the database.
        """
        await self.db.delete(user)

    async def get_by_email_and_organization(
        self,
        email: str,
        organization_id: UUID,
    ) -> User | None:
        statement = (
            select(User)
            .where(User.email == email)
            .where(User.organization_id == organization_id)
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
