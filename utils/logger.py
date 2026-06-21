"""
Logger setup and configuration
"""
import sys
from pathlib import Path
from loguru import logger

from config import get_settings

settings = get_settings()

# Remove default handler
logger.remove()

# Add console handler
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.log_level,
    colorize=True,
)

# Add file handler
log_file = Path(settings.log_file)
log_file.parent.mkdir(parents=True, exist_ok=True)

logger.add(
    log_file,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="500 MB",
    retention="10 days",
)

__all__ = ["logger"]
