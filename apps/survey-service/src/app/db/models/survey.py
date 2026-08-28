from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.models.model_base import BaseModel


class Survey(BaseModel):
    __tablename__ = "surveys"

    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    created_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    organization: Mapped["Organization"] = relationship(back_populates="surveys", lazy="selectin")
    questions: Mapped[list["SurveyQuestion"]] = relationship(
        back_populates="survey",
        cascade="all, delete-orphan",
        order_by="SurveyQuestion.order",
        lazy="selectin",
    )
