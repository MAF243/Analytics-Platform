import sys

from loguru import logger

from backend.app.core.config import settings


def setup_logging() -> None:
    """Configures structured JSON logging with Loguru."""
    logger.remove()

    log_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        "{name}:{function}:{line} | {message} | {extra}"
    )

    if settings.env == "production":
        logger.add(
            sys.stdout, format="{message}", level=settings.log_level, serialize=True
        )
    else:
        logger.add(
            sys.stdout,
            format=log_format,
            level=settings.log_level,
            colorize=True,
        )

    logger.info(f"Logging initialized at level {settings.log_level}")
