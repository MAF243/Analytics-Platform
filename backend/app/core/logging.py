import sys
import time
from typing import Any

from loguru import logger

from backend.app.core.config import settings


def inject_processing_time(record: dict[str, Any]) -> None:
    """Patcher to automatically compute and inject processing_time_ms if start_time is bound."""
    if "start_time" in record["extra"]:
        start_time = record["extra"]["start_time"]
        record["extra"]["processing_time_ms"] = round(
            (time.perf_counter() - start_time) * 1000, 2
        )


def setup_logging() -> None:
    """Configures structured JSON logging with Loguru."""
    logger.remove()

    logger.configure(patcher=inject_processing_time)  # type: ignore

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

    logger.info(
        f"Logging initialized at level {settings.log_level}",
        event="logging.initialized",
    )
