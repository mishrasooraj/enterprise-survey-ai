from jose import JWTError
from jose import jwt

from app.core.core_config import settings


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None

