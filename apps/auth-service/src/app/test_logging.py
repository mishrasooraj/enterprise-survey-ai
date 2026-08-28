from app.core.core_logging import configure_logging, logger

configure_logging()

logger.debug("Debug message")
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
