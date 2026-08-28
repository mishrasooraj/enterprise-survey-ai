from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient

from app.auth_service_main import app
from app.events.event_producer import InMemoryEventProducer


def _survey_payload(organization_id):
    now = datetime.now(timezone.utc)
    return {
        "id": str(uuid4()),
        "organization_id": str(organization_id),
        "title": "Customer Feedback",
        "description": "Annual survey",
        "status": "draft",
        "created_by": str(uuid4()),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "questions": [],
    }


def test_create_get_update_delete_survey(monkeypatch):
    org_id = uuid4()
    user = {"sub": str(uuid4()), "organization_id": str(org_id), "role": "admin", "permissions": ["surveys:write"], "is_active": True}
    survey = SimpleNamespace(**_survey_payload(org_id))
    producer = InMemoryEventProducer()

    async def fake_get_current_user():
        return user

    async def fake_list_surveys(self, organization_id):
        return [survey]

    async def fake_get_by_id(self, survey_id):
        return survey

    async def fake_update_survey(self, existing, payload):
        return survey

    async def fake_delete_survey(self, existing):
        return None

    from app.dependencies import auth_dependency
    from app.repositories import survey_repository
    from app.services import survey_service
    from app.dependencies import event_dependency

    app.dependency_overrides[auth_dependency.get_current_user] = fake_get_current_user
    app.dependency_overrides[event_dependency.get_event_producer] = lambda: producer
    async def fake_repo_create(self, survey_obj):
        return survey

    monkeypatch.setattr(survey_repository.SurveyRepository, "create", fake_repo_create)
    monkeypatch.setattr(survey_service.SurveyService, "list_surveys", fake_list_surveys)
    monkeypatch.setattr(survey_service.SurveyService, "update_survey", fake_update_survey)
    monkeypatch.setattr(survey_service.SurveyService, "delete_survey", fake_delete_survey)
    monkeypatch.setattr(survey_repository.SurveyRepository, "get_by_id", fake_get_by_id)

    client = TestClient(app)

    create_response = client.post(
        "/api/v1/surveys",
        json={
            "organization_id": str(org_id),
            "title": "Customer Feedback",
            "description": "Annual survey",
            "status": "draft",
            "questions": [],
        },
    )
    assert create_response.status_code == 201
    assert create_response.json()["organization_id"] == str(org_id)
    assert producer.events and producer.events[0].event_type.value == "survey.created"

    list_response = client.get("/api/v1/surveys")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/api/v1/surveys/{survey.id}")
    assert get_response.status_code == 200

    patch_response = client.patch(
        f"/api/v1/surveys/{survey.id}",
        json={"title": "Updated"},
    )
    assert patch_response.status_code == 200

    delete_response = client.delete(f"/api/v1/surveys/{survey.id}")
    assert delete_response.status_code == 204

    app.dependency_overrides.clear()


def test_tenant_isolation_blocks_cross_org(monkeypatch):
    org_id = uuid4()
    other_org_id = uuid4()
    user = {"sub": str(uuid4()), "organization_id": str(other_org_id), "role": "admin", "permissions": ["surveys:write"], "is_active": True}

    async def fake_get_current_user():
        return user

    from app.dependencies import auth_dependency
    from app.dependencies import event_dependency

    app.dependency_overrides[auth_dependency.get_current_user] = fake_get_current_user
    app.dependency_overrides[event_dependency.get_event_producer] = lambda: InMemoryEventProducer()

    client = TestClient(app)
    response = client.post(
        "/api/v1/surveys",
        json={
            "organization_id": str(org_id),
            "title": "Blocked",
            "description": None,
            "status": "draft",
            "questions": [],
        },
    )
    assert response.status_code == 403
    app.dependency_overrides.clear()
