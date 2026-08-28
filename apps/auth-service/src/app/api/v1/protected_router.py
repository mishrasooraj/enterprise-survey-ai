from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.authz_dependency import get_authenticated_user
from app.dependencies.authz_dependency import require_organization_match
from app.dependencies.authz_dependency import require_permission
from app.dependencies.authz_dependency import require_role
from app.db.models.user import User

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/authenticated")
async def authenticated_endpoint(
    current_user: User = Depends(get_authenticated_user),
) -> dict[str, str]:
    return {
        "message": "Authenticated access granted.",
        "user_id": str(current_user.id),
    }


@router.get("/admin")
async def admin_only_endpoint(
    current_user: User = Depends(require_role("Admin")),
) -> dict[str, str]:
    return {
        "message": "Admin access granted.",
        "user_id": str(current_user.id),
    }


@router.get("/permissions/surveys:write")
async def survey_write_endpoint(
    current_user: User = Depends(require_permission("surveys:write")),
) -> dict[str, str]:
    return {
        "message": "Permission granted.",
        "user_id": str(current_user.id),
    }


@router.get("/tenants/{organization_id}")
async def tenant_scoped_endpoint(
    organization_id: UUID,
    current_user: User = Depends(require_organization_match(organization_id)),
) -> dict[str, str]:
    return {
        "message": "Tenant access granted.",
        "organization_id": str(current_user.organization_id),
    }
