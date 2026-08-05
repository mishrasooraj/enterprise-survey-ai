from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """
    Request body for user registration.
    """

    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )
    full_name: str = Field(
        min_length=2,
        max_length=100,
    )


class UserLoginRequest(BaseModel):
    """
    Request body for login.
    """

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    JWT tokens returned after authentication.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Data stored inside the JWT.
    """

    sub: UUID
    email: EmailStr
    