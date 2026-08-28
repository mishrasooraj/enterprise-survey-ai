from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_deps import get_db
from app.core.core_jwt import decode_refresh_token
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import (
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthenticationService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/health")
async def health_check() -> dict[str, str]:
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
    service = AuthenticationService(
        db=db,
        user_repository=UserRepository(db),
        organization_repository=OrganizationRepository(db),
        role_repository=RoleRepository(db),
        permission_repository=PermissionRepository(db),
    )

    try:
        user = await service.register(request)
        return UserResponse.model_validate(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    service = AuthenticationService(
        db=db,
        user_repository=UserRepository(db),
        organization_repository=OrganizationRepository(db),
        role_repository=RoleRepository(db),
        permission_repository=PermissionRepository(db),
    )

    result = await service.authenticate(request)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return LoginResponse(
        message="Login successful.",
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        user=UserResponse.model_validate(
            result["user"],
        ),
    )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_tokens(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> RefreshTokenResponse:
    service = AuthenticationService(
        db=db,
        user_repository=UserRepository(db),
        organization_repository=OrganizationRepository(db),
        role_repository=RoleRepository(db),
        permission_repository=PermissionRepository(db),
    )
    payload = decode_refresh_token(request.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        )
    user = await UserRepository(db).get_by_id(UUID(payload["sub"]))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    tokens = await service.refresh_tokens(user)
    return RefreshTokenResponse(**tokens)
