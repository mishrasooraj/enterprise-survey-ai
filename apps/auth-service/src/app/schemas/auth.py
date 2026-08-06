from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field

from app.schemas.user import UserResponse


class UserRegisterRequest(BaseModel):
    """
    Request body for user registration.
    """

    company_name: str = Field(
        min_length=2,
        max_length=255,
    )

    company_slug: str = Field(
        min_length=2,
        max_length=100,
        pattern=r"^[a-z0-9-]+$",
    )

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
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


class LoginResponse(BaseModel):
    """
    Response returned after successful authentication.
    """

    message: str
    user: UserResponse


class RegisterResponse(BaseModel):
    """
    Response returned after successful registration.
    """

    message: str
    user: UserResponse

    model_config = ConfigDict(
        from_attributes=True,
    )