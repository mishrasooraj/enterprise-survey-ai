from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.models.base import BaseModel


class User(BaseModel):
    """
    User entity.
    """

    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )