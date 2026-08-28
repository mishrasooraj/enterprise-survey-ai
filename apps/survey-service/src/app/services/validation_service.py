from app.schemas.survey_generation_schema import GeneratedSurveyDraft
from app.schemas.survey_generation_schema import SurveyGenerationValidationError


class SurveyValidationService:
    allowed_question_types = {
        "short_text",
        "long_text",
        "single_choice",
        "multiple_choice",
        "rating",
        "yes_no",
        "number",
    }

    def validate(self, draft: GeneratedSurveyDraft) -> GeneratedSurveyDraft:
        if not draft.title.strip():
            raise SurveyGenerationValidationError("Survey title cannot be empty.")
        if not draft.questions:
            raise SurveyGenerationValidationError("Generated survey must include at least one question.")

        seen_orders: set[int] = set()
        for question in draft.questions:
            if question.question_type not in self.allowed_question_types:
                raise SurveyGenerationValidationError(f"Unsupported question type: {question.question_type}")
            if question.order in seen_orders:
                raise SurveyGenerationValidationError("Question order values must be unique.")
            seen_orders.add(question.order)
            if question.question_type in {"single_choice", "multiple_choice"} and not question.options:
                raise SurveyGenerationValidationError("Choice questions must include options.")
            if question.question_type not in {"single_choice", "multiple_choice"} and question.options:
                raise SurveyGenerationValidationError("Only choice questions may include options.")

        draft.questions = sorted(draft.questions, key=lambda item: item.order)
        return draft

