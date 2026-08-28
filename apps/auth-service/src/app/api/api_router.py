from fastapi import APIRouter

from app.api.v1.auth_router import router as auth_router
from app.api.v1.protected_router import router as protected_router
from app.api.v1.users import router as users_router


api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(protected_router)
