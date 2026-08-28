from __future__ import annotations

from typing import Any

from app.schemas.survey_generation_schema import GeneratedSurveyDraft


def build_openai_structured_client() -> Any:
    try:
        from langchain_openai import ChatOpenAI
    except Exception as exc:  # pragma: no cover - optional dependency guard
        raise RuntimeError("langchain-openai is not installed.") from exc

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return model.with_structured_output(GeneratedSurveyDraft)

