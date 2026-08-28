from uuid import uuid4

import pytest
from fastapi import HTTPException
from jose import jwt

from app.core.core_config import settings
from app.dependencies import auth_dependency as survey_auth


def make_token(payload: dict) -> str:
    return jwt.encode(payload, settings.jwt.secret_key or "test-secret", algorithm=settings.jwt.algorithm)


@pytest.mark.asyncio
async def test_valid_jwt(monkeypatch):
    monkeypatch.setattr(settings, "jwt_secret_key", "test-secret")
    payload = {"sub": "user-1", "organization_id": "org-1", "role": "admin", "permissions": ["surveys:write"], "is_active": True, "type": "access"}
    token = make_token(payload)
    class Credentials:
        credentials = token

    result = await survey_auth.get_current_user(credentials=Credentials())
    assert result["sub"] == "user-1"


@pytest.mark.asyncio
async def test_invalid_jwt(monkeypatch):
    monkeypatch.setattr(settings, "jwt_secret_key", "test-secret")
    with pytest.raises(HTTPException):
        class Credentials:
            credentials = "bad-token"
        await survey_auth.get_current_user(credentials=Credentials())


@pytest.mark.asyncio
async def test_inactive_user(monkeypatch):
    monkeypatch.setattr(settings, "jwt_secret_key", "test-secret")
    payload = {"sub": "user-1", "organization_id": "org-1", "role": "admin", "permissions": [], "is_active": False, "type": "access"}
    token = make_token(payload)
    with pytest.raises(HTTPException) as exc_info:
        class Credentials:
            credentials = token
        await survey_auth.get_current_user(credentials=Credentials())
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_wrong_organization():
    dependency = survey_auth.require_organization_access()
    with pytest.raises(HTTPException) as exc_info:
        await dependency(
            organization_id=uuid4(),
            current_user={"organization_id": "other-org"},
        )
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_missing_permission():
    dependency = survey_auth.require_permission("surveys:write")
    with pytest.raises(HTTPException) as exc_info:
        await dependency(current_user={"permissions": ["surveys:read"], "sub": "user-1"})
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_valid_permission():
    dependency = survey_auth.require_permission("surveys:write")
    result = await dependency(current_user={"permissions": ["surveys:write"], "sub": "user-1"})
    assert result["sub"] == "user-1"


@pytest.mark.asyncio
async def test_valid_admin_access():
    dependency = survey_auth.require_role("admin")
    result = await dependency(current_user={"role": "admin", "sub": "user-1"})
    assert result["sub"] == "user-1"
