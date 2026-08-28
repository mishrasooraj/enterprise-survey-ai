from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.core_jwt import (
    create_access_token,
    create_refresh_token,
)

from app.core.core_security import (
    hash_password,
    verify_password,
)

from app.db.models.organization import Organization
from app.db.models.user import User

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository

from app.schemas.auth_schema import (
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
        permission_repository: PermissionRepository | None = None,
    ):
        self.db = db
        self.user_repository = user_repository
        self.organization_repository = organization_repository
        self.role_repository = role_repository
        self.permission_repository = permission_repository

    async def register(self, request: UserRegisterRequest) -> User:
        """
        Register a new organization and its first admin user.
        """

        existing_user = await self.user_repository.get_by_email(request.email)

        if existing_user:
            raise ValueError(
                "User with this email already exists."
            )

        existing_organization = await self.organization_repository.get_by_slug(
            request.company_slug
        )

        if existing_organization:
            raise ValueError(
                "Organization with this slug already exists."
            )

        try:
            organization = await self.organization_repository.create(
                Organization(
                    name=request.company_name,
                    slug=request.company_slug,
                    is_active=True,
                )
            )
            await self.role_repository.create_default_roles(organization.id)
            admin_role = await self.role_repository.get_by_name(organization.id, "Admin")
            if admin_role is None:
                raise ValueError("Failed to create Admin role.")

            user = await self.user_repository.create(
                User(
                    full_name=request.full_name,
                    email=request.email,
                    password_hash=hash_password(request.password),
                    is_active=True,
                    is_verified=False,
                    organization_id=organization.id,
                    role_id=admin_role.id,
                )
            )
            await self.db.commit()
            return user
        except Exception:
            await self.db.rollback()
            raise

    async def authenticate(self, request: UserLoginRequest) -> dict[str, User | str] | None:
        """
        Authenticate a user.
        """

        user = await self.user_repository.get_by_email(request.email)

        if user is None:
            return None

        if not user.is_active:
            return None
        if not verify_password(request.password, user.password_hash):
            return None

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "organization_id": str(user.organization_id),
            "role_id": str(user.role_id),
        }

        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def refresh_tokens(self, user: User) -> dict[str, str]:
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "organization_id": str(user.organization_id),
            "role_id": str(user.role_id),
        }
        user.last_login = datetime.now(timezone.utc)
        await self.db.flush()
        return {
            "access_token": create_access_token(payload),
            "refresh_token": create_refresh_token(payload),
        }
