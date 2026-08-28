from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.schemas.auth_schema import UserLoginRequest, UserRegisterRequest
from app.services.auth_service import AuthenticationService


class FakeRepo:
    def __init__(self, value=None):
        self.value = value
        self.created = []
        self.slugs = set()

    async def get_by_email(self, email):
        return self.value if getattr(self.value, "email", None) == email else None

    async def get_by_slug(self, slug):
        return self.value if getattr(self.value, "slug", None) == slug else None

    async def create(self, obj):
        self.created.append(obj)
        return obj

    async def create_default_roles(self, organization_id):
        admin_role = SimpleNamespace(id=uuid4(), name="Admin", organization_id=organization_id, permissions=[])
        self.value = admin_role
        return [admin_role]

    async def get_by_name(self, organization_id, name):
        if getattr(self.value, "name", None) == name:
            return self.value
        return None

    async def get_by_id(self, role_id):
        return self.value


class FakeDB:
    def __init__(self):
        self.committed = False
        self.rolled_back = False
        self.flushed = False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

    async def flush(self):
        self.flushed = True


@pytest.mark.asyncio
async def test_register_creates_user_and_org(monkeypatch):
    db = FakeDB()
    org_repo = FakeRepo()
    role_repo = FakeRepo()
    user_repo = FakeRepo()
    service = AuthenticationService(
        db=db,
        user_repository=user_repo,
        organization_repository=org_repo,
        role_repository=role_repo,
    )
    request = UserRegisterRequest(
        company_name="Acme",
        company_slug="acme",
        full_name="Admin User",
        email="admin@acme.com",
        password="Password123!",
    )

    async def fake_org_create(org):
        org.id = uuid4()
        return org

    async def fake_user_create(user):
        user.id = uuid4()
        return user

    monkeypatch.setattr(org_repo, "create", fake_org_create)
    async def fake_create_default_roles(organization_id):
        return None

    async def fake_get_by_name(organization_id, name):
        return SimpleNamespace(id=uuid4(), name=name)

    monkeypatch.setattr(role_repo, "create_default_roles", fake_create_default_roles)
    monkeypatch.setattr(role_repo, "get_by_name", fake_get_by_name)
    monkeypatch.setattr(user_repo, "create", fake_user_create)

    user = await service.register(request)

    assert user.email == "admin@acme.com"
    assert db.committed is True
    assert db.rolled_back is False


@pytest.mark.asyncio
async def test_authenticate_returns_tokens(monkeypatch):
    db = FakeDB()
    user = SimpleNamespace(
        id=uuid4(),
        email="admin@acme.com",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$dummy$dummy",
        organization_id=uuid4(),
        role_id=uuid4(),
        is_active=True,
    )
    user_repo = FakeRepo(user)
    service = AuthenticationService(
        db=db,
        user_repository=user_repo,
        organization_repository=FakeRepo(),
        role_repository=FakeRepo(),
    )

    monkeypatch.setattr("app.services.auth_service.verify_password", lambda plain, hashed: True)
    monkeypatch.setattr("app.services.auth_service.create_access_token", lambda payload: "access-token")
    monkeypatch.setattr("app.services.auth_service.create_refresh_token", lambda payload: "refresh-token")

    result = await service.authenticate(
        UserLoginRequest(email="admin@acme.com", password="Password123!")
    )

    assert result is not None
    assert result["access_token"] == "access-token"
    assert result["refresh_token"] == "refresh-token"
