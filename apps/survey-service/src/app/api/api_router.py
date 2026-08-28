from fastapi import APIRouter

from app.api.v1.survey_router import router as survey_router
from app.api.v1.protected_router import router as protected_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(survey_router)
api_router.include_router(protected_router)
