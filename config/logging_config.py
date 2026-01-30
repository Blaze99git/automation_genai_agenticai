from loguru import logger
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logging():
    logger.remove()

    # Console logs (colored, readable)
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | "
               "<level>{level}</level> | "
               "<cyan>{name}</cyan> | "
               "{message}"
    )

    # File logs (detailed, persistent)
    logger.add(
        LOG_DIR / "app.log",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        format="{time} | {level} | {name}:{function}:{line} | {message}"
    )

    return logger