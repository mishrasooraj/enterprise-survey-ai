from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.permission import Permission


class PermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> Permission | None:
        result = await self.db.execute(select(Permission).where(Permission.name == name))
        return result.scalar_one_or_none()

    async def create(self, permission: Permission) -> Permission:
        self.db.add(permission)
        await self.db.flush()
        await self.db.refresh(permission)
        return permission
