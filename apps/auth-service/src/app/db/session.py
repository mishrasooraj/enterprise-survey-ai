from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# ======================================================
# SQLAlchemy Async Engine
# ======================================================

engine = create_async_engine(
    settings.database.url,
    echo=settings.app.env == "development",
)

# ======================================================
# Async Session Factory
# ======================================================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)