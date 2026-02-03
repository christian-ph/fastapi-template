from .custom_logger import CustomLogger
from app.infrastructure.config import Settings

settings = Settings.load_configs()

# Create default logger instance configured from settings
logger = CustomLogger(
    name=settings.LOG_NAME,
    level=settings.LOG_LEVEL
)._logger

__all__ = ['CustomLogger', 'logger']
