from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.auth_dependency import get_current_user
from app.dependencies.auth_dependency import require_permission
from app.dependencies.auth_dependency import require_role


router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/authenticated")
async def authenticated_access(current_user: dict = Depends(get_current_user)) -> dict[str, str]:
    return {"message": "authenticated", "sub": current_user["sub"]}


@router.get("/admin")
async def admin_access(current_user: dict = Depends(require_role("admin"))) -> dict[str, str]:
    return {"message": "admin", "sub": current_user["sub"]}


@router.get("/permission")
async def permission_access(current_user: dict = Depends(require_permission("surveys:write"))) -> dict[str, str]:
    return {"message": "permission", "sub": current_user["sub"]}
