from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jose import JWTError
from jose import jwt

from app.core.core_config import settings


def _require_secret(secret: str) -> str:
    if not secret:
        raise RuntimeError("JWT secret key is not configured.")
    return secret


def create_token(payload: dict, expires_delta: timedelta, token_type: str) -> str:
    """
    Create a JWT token with an expiration time.
    """

    token_payload = payload.copy()
    token_payload.update(
        {
            "exp": datetime.now(timezone.utc) + expires_delta,
            "iat": datetime.now(timezone.utc),
            "jti": str(uuid4()),
            "type": token_type,
        }
    )

    return jwt.encode(
        token_payload,
        _require_secret(
            settings.jwt_refresh_secret if token_type == "refresh" else settings.jwt.secret_key
        ),
        algorithm=settings.jwt.algorithm,
    )


def create_access_token(payload: dict) -> str:
    return create_token(
        payload,
        timedelta(minutes=settings.jwt.access_token_expire_minutes),
        "access",
    )


def create_refresh_token(payload: dict) -> str:
    return create_token(
        payload,
        timedelta(days=settings.jwt.refresh_token_expire_days),
        "refresh",
    )


def decode_token(token: str, token_type: str) -> dict | None:
    try:
        secret = settings.jwt_refresh_secret if token_type == "refresh" else settings.jwt.secret_key
        payload = jwt.decode(
            token,
            _require_secret(secret),
            algorithms=[settings.jwt.algorithm],
        )
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None


def decode_access_token(token: str) -> dict | None:
    return decode_token(token, "access")


def decode_refresh_token(token: str) -> dict | None:
    return decode_token(token, "refresh")
