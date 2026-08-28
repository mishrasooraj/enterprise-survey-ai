from datetime import datetime, timezone

import pytest

from app.core import core_jwt as jwt_module


def test_create_and_decode_access_token(monkeypatch):
    monkeypatch.setattr(jwt_module.settings, "jwt_secret_key", "test-access-secret")
    monkeypatch.setattr(jwt_module.settings, "jwt_refresh_secret_key", "test-refresh-secret")

    token = jwt_module.create_access_token({"sub": "user-123", "email": "a@example.com"})
    payload = jwt_module.decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "user-123"
    assert payload["email"] == "a@example.com"
    assert payload["type"] == "access"
    assert "exp" in payload
    assert "jti" in payload


def test_create_and_decode_refresh_token(monkeypatch):
    monkeypatch.setattr(jwt_module.settings, "jwt_secret_key", "test-access-secret")
    monkeypatch.setattr(jwt_module.settings, "jwt_refresh_secret_key", "test-refresh-secret")

    token = jwt_module.create_refresh_token({"sub": "user-123"})
    payload = jwt_module.decode_refresh_token(token)

    assert payload is not None
    assert payload["type"] == "refresh"


def test_decode_rejects_wrong_token_type(monkeypatch):
    monkeypatch.setattr(jwt_module.settings, "jwt_secret_key", "test-access-secret")
    monkeypatch.setattr(jwt_module.settings, "jwt_refresh_secret_key", "test-refresh-secret")

    token = jwt_module.create_access_token({"sub": "user-123"})
    assert jwt_module.decode_refresh_token(token) is None
