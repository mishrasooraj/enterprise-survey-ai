from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.dependencies import auth_dependency
from app.dependencies import authz_dependency


class FakeResult:
    def __init__(self, value):
        self.value = value

    def scalar_one_or_none(self):
        return self.value


class FakeDB:
    def __init__(self, user):
        self.user = user

    async def execute(self, statement):
        return FakeResult(self.user)


def build_user(role_name="Admin", permissions=None, is_active=True, organization_id=None):
    organization_id = organization_id or uuid4()
    role = SimpleNamespace(
        name=role_name,
        permissions=[
            SimpleNamespace(name=name, is_active=True) for name in (permissions or [])
        ],
    )
    return SimpleNamespace(
        id=uuid4(),
        is_active=is_active,
        organization_id=organization_id,
        role=role,
    )


@pytest.mark.asyncio
async def test_valid_jwt_returns_user(monkeypatch):
    user = build_user()

    monkeypatch.setattr(auth_dependency, "decode_access_token", lambda token: {"sub": str(user.id)})

    async def get_by_id(_user_id):
        return user

    monkeypatch.setattr(auth_dependency, "UserRepository", lambda db: SimpleNamespace(get_by_id=get_by_id))

    result = await auth_dependency.get_current_user(
        credentials=SimpleNamespace(credentials="token"),
        db=SimpleNamespace(),
    )

    assert result.id == user.id


@pytest.mark.asyncio
async def test_invalid_jwt_rejected(monkeypatch):
    monkeypatch.setattr(auth_dependency, "decode_access_token", lambda token: None)

    with pytest.raises(HTTPException) as exc_info:
        await auth_dependency.get_current_user(
            credentials=SimpleNamespace(credentials="bad-token"),
            db=SimpleNamespace(),
        )

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_inactive_user_rejected(monkeypatch):
    user = build_user(is_active=False)

    monkeypatch.setattr(auth_dependency, "decode_access_token", lambda token: {"sub": str(user.id)})

    async def get_by_id(_user_id):
        return user

    monkeypatch.setattr(auth_dependency, "UserRepository", lambda db: SimpleNamespace(get_by_id=get_by_id))

    with pytest.raises(HTTPException) as exc_info:
        await auth_dependency.get_current_user(
            credentials=SimpleNamespace(credentials="token"),
            db=SimpleNamespace(),
        )

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_wrong_organization_rejected(monkeypatch):
    org_a = uuid4()
    org_b = uuid4()
    user = build_user(organization_id=org_a)

    async def load_access_context(_db, _user_id):
        return authz_dependency.AccessContext(
            user=user,
            organization_id=org_a,
            role_name="Admin",
            permissions=frozenset(),
        )

    monkeypatch.setattr(authz_dependency, "_load_access_context", load_access_context)

    dep = authz_dependency.require_organization_match(org_b)
    with pytest.raises(HTTPException) as exc_info:
        await dep(current_user=user)

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_missing_permission_rejected(monkeypatch):
    user = build_user(role_name="Manager", permissions={"surveys:read"})
    async def load_access_context(_db, _user_id):
        return authz_dependency.AccessContext(
            user=user,
            organization_id=user.organization_id,
            role_name=user.role.name,
            permissions=frozenset({"surveys:read"}),
        )

    monkeypatch.setattr(authz_dependency, "_load_access_context", load_access_context)

    dep = authz_dependency.require_permission("surveys:write")
    with pytest.raises(HTTPException) as exc_info:
        await dep(current_user=user)

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_valid_permission_allowed(monkeypatch):
    user = build_user(role_name="Manager", permissions={"surveys:write"})
    async def load_access_context(_db, _user_id):
        return authz_dependency.AccessContext(
            user=user,
            organization_id=user.organization_id,
            role_name=user.role.name,
            permissions=frozenset({"surveys:write"}),
        )

    monkeypatch.setattr(authz_dependency, "_load_access_context", load_access_context)

    dep = authz_dependency.require_permission("surveys:write")
    result = await dep(current_user=user)

    assert result.id == user.id


@pytest.mark.asyncio
async def test_valid_admin_access_allowed(monkeypatch):
    user = build_user(role_name="Admin", permissions={"surveys:write"})
    async def load_access_context(_db, _user_id):
        return authz_dependency.AccessContext(
            user=user,
            organization_id=user.organization_id,
            role_name="Admin",
            permissions=frozenset({"surveys:write"}),
        )

    monkeypatch.setattr(authz_dependency, "_load_access_context", load_access_context)

    dep = authz_dependency.require_role("Admin")
    result = await dep(current_user=user)

    assert result.id == user.id
