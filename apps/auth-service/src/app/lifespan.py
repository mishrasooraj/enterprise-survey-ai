from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan events.
    """

    configure_logging()

    logger.info("=" * 60)
    logger.info("Starting %s", settings.app.name)
    logger.info("Environment : %s", settings.app.env)
    logger.info("Version     : %s", settings.app.version)
    logger.info("=" * 60)

    try:
        yield

    finally:
        logger.info("Shutting down %s", settings.app.name)