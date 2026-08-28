from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_deps import get_db
from app.core.core_jwt import decode_access_token
from app.db.models.survey import Survey
from app.repositories.survey_repository import SurveyRepository


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if payload.get("is_active") is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def require_role(role_name: str):
    async def _dependency(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") != role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role.",
            )
        return current_user

    return _dependency


def require_permission(permission_name: str):
    async def _dependency(current_user: dict = Depends(get_current_user)) -> dict:
        permissions = set(current_user.get("permissions", []))
        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )
        return current_user

    return _dependency


def require_organization_access():
    async def _dependency(
        organization_id: UUID,
        current_user: dict = Depends(get_current_user),
    ) -> dict:
        if current_user.get("organization_id") != str(organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cross-tenant access is not allowed.",
            )
        return current_user

    return _dependency


def require_survey_access():
    async def _dependency(
        survey_id: UUID,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> Survey:
        survey = await SurveyRepository(db).get_by_id(survey_id)
        if survey is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Survey not found.",
            )
        if str(survey.organization_id) != current_user.get("organization_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cross-tenant access is not allowed.",
            )
        return survey

    return _dependency
