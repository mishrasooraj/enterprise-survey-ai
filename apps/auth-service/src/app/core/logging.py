import logging
import sys

from app.core.config import settings


def configure_logging() -> None:
    """
    Configure application logging.
    """

    logging.basicConfig(
        level=settings.app.log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        force=True,
    )


logger = logging.getLogger("auth-service")