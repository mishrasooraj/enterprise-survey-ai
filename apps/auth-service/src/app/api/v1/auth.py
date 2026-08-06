from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.repositories.organization import OrganizationRepository
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas.auth import (
    LoginResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from app.schemas.user import UserResponse
from app.services.auth import AuthenticationService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "service": "auth-service",
    }


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: UserRegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Register a new organization and its first admin user.
    """

    service = AuthenticationService(
        db=db,
        user_repository=UserRepository(db),
        organization_repository=OrganizationRepository(db),
        role_repository=RoleRepository(db),
    )

    try:
        user = await service.register(request)

        return UserResponse.model_validate(user)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    """
    Authenticate a user.
    """

    service = AuthenticationService(
        db=db,
        user_repository=UserRepository(db),
        organization_repository=OrganizationRepository(db),
        role_repository=RoleRepository(db),
    )

    user = await service.authenticate(request)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return LoginResponse(
        message="Login successful.",
        user=UserResponse.model_validate(user),
    )