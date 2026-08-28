from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.api_deps import get_db
from app.dependencies.auth_dependency import get_current_user
from app.db.models.role import Role
from app.db.models.user import User


@dataclass(frozen=True, slots=True)
class AccessContext:
    user: User
    organization_id: UUID
    role_name: str
    permissions: frozenset[str]


async def _load_access_context(db: AsyncSession, user_id: UUID) -> AccessContext:
    statement = (
        select(User)
        .options(
            selectinload(User.role).selectinload(Role.permissions),
        )
        .where(User.id == user_id)
    )
    result = await db.execute(statement)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    permissions = frozenset(
        permission.name for permission in (user.role.permissions or [])
        if getattr(permission, "is_active", True)
    )
    return AccessContext(
        user=user,
        organization_id=user.organization_id,
        role_name=user.role.name,
        permissions=permissions,
    )


async def get_authenticated_user(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    await _load_access_context(db, current_user.id)
    return current_user


def require_organization_match(organization_id: UUID):
    async def _dependency(
        current_user: User = Depends(get_authenticated_user),
    ) -> User:
        if current_user.organization_id != organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cross-tenant access is not allowed.",
            )
        return current_user

    return _dependency


def require_role(role_name: str):
    async def _dependency(
        current_user: User = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        context = await _load_access_context(db, current_user.id)
        if context.role_name != role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role.",
            )
        return current_user

    return _dependency


def require_permission(permission_name: str):
    async def _dependency(
        current_user: User = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        context = await _load_access_context(db, current_user.id)
        if permission_name not in context.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )
        return current_user

    return _dependency


def require_role_or_permission(role_name: str, permission_name: str):
    async def _dependency(
        current_user: User = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        context = await _load_access_context(db, current_user.id)
        if context.role_name != role_name and permission_name not in context.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )
        return current_user

    return _dependency
