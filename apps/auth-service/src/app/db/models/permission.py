from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.models.base import BaseModel


class Permission(BaseModel):
    """
    Permission entity.
    """

    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )