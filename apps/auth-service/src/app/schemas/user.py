from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr

    is_active: bool
    is_verified: bool

    organization_id: UUID
    role_id: UUID

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
