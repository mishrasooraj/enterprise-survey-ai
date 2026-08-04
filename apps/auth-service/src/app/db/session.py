from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# ======================================================
# SQLAlchemy Engine
# ======================================================

engine = create_engine(
    settings.database.url,
    echo=settings.app.env == "development",
    future=True,
)

# ======================================================
# Session Factory
# ======================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# ======================================================
# Dependency
# ======================================================

def get_db() -> Generator[Session, None, None]:
    """
    Provides a database session per request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()