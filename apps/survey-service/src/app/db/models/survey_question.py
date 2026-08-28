from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.models.model_base import BaseModel


class SurveyQuestion(BaseModel):
    __tablename__ = "survey_questions"

    survey_id: Mapped[UUID] = mapped_column(ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(50), nullable=False)
    options: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    survey: Mapped["Survey"] = relationship(back_populates="questions", lazy="selectin")

