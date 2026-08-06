from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
)
from app.db.models.organization import Organization
from app.db.models.user import User
from app.repositories.organization import OrganizationRepository
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas.auth import (
    UserLoginRequest,
    UserRegisterRequest,
)


class AuthenticationService:
    """
    Business logic for authentication.
    """

    def __init__(
        self,
        db: AsyncSession,
        user_repository: UserRepository,
        organization_repository: OrganizationRepository,
        role_repository: RoleRepository,
    ):
        self.db = db
        self.user_repository = user_repository
        self.organization_repository = organization_repository
        self.role_repository = role_repository

    async def register(
        self,
        request: UserRegisterRequest,
    ) -> User:
        """
        Register a new organization and its first admin user.
        """

        # ----------------------------------------
        # Check if email already exists
        # ----------------------------------------

        existing_user = await self.user_repository.get_by_email(
            request.email,
        )

        if existing_user:
            raise ValueError(
                "User with this email already exists."
            )

        # ----------------------------------------
        # Check if organization slug already exists
        # ----------------------------------------

        existing_organization = (
            await self.organization_repository.get_by_slug(
                request.company_slug,
            )
        )

        if existing_organization:
            raise ValueError(
                "Organization with this slug already exists."
            )

        try:

            # ----------------------------------------
            # Create organization
            # ----------------------------------------

            organization = Organization(
                name=request.company_name,
                slug=request.company_slug,
                is_active=True,
            )

            organization = await (
                self.organization_repository.create(
                    organization,
                )
            )

            # ----------------------------------------
            # Create default roles
            # ----------------------------------------

            await self.role_repository.create_default_roles(
                organization.id,
            )

            # ----------------------------------------
            # Fetch Admin role
            # ----------------------------------------

            admin_role = await self.role_repository.get_by_name(
                organization.id,
                "Admin",
            )

            if admin_role is None:
                raise ValueError(
                    "Failed to create Admin role."
                )

            # ----------------------------------------
            # Create first admin user
            # ----------------------------------------

            user = User(
                full_name=request.full_name,
                email=request.email,
                password_hash=hash_password(
                    request.password,
                ),
                is_active=True,
                is_verified=False,
                organization_id=organization.id,
                role_id=admin_role.id,
            )

            user = await self.user_repository.create(
                user,
            )

            # ----------------------------------------
            # Commit transaction
            # ----------------------------------------

            await self.db.commit()

            return user

        except Exception:

            await self.db.rollback()

            raise

    async def authenticate(
        self,
        request: UserLoginRequest,
    ) -> User | None:
        """
        Authenticate a user.
        """

        user = await self.user_repository.get_by_email(
            request.email,
        )

        if user is None:
            return None

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            return None

        return user 