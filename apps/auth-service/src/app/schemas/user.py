from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    """
    User information returned to clients.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str
    is_active: bool
    organization_id: UUID
    role_id: UUID
    created_at: datetime