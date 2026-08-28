from app.schemas.survey_generation_schema import SurveyGenerationRequest


class SurveyPromptService:
    def build_system_prompt(self) -> str:
        return (
            "You are an expert enterprise survey designer. "
            "Return only structured JSON that matches the required schema. "
            "The output must be deterministic in structure: include title, description, status, and an ordered questions array."
        )

    def build_user_prompt(self, request: SurveyGenerationRequest) -> str:
        return (
            f"Business requirement: {request.business_requirement}\n"
            f"Organization: {request.organization_name}\n"
            f"Organization summary: {request.organization_summary}\n"
            f"Target audience: {request.target_audience}\n"
            f"Desired question count: {request.desired_question_count}\n"
            f"Tone: {request.tone}\n"
            "Generate a survey draft that is practical, complete, and ordered from broad context to specific follow-up questions."
        )

