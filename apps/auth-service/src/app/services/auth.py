from uuid import uuid4

from app.core.security import (
    hash_password,
    verify_password,
)
from app.db.models.user import User
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
        repository: UserRepository,
    ):
        self.repository = repository

    async def register(
        self,
        request: UserRegisterRequest,
    ) -> User:
        """
        Register a new user.
        """

        existing_user = await self.repository.get_by_email(
            request.email,
        )

        if existing_user:
            raise ValueError(
                "User with this email already exists."
            )

        user = User(
            email=request.email,
            full_name=request.full_name,
            password_hash=hash_password(
                request.password,
            ),
            is_active=True,
            organization_id=uuid4(),
            role_id=uuid4(),
        )

        return await self.repository.create(user)

    async def authenticate(
        self,
        request: UserLoginRequest,
    ) -> User | None:
        """
        Authenticate a user.
        """

        user = await self.repository.get_by_email(
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