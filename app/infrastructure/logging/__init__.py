import logging

from app.infrastructure.config import Settings

from .custom_logger import CustomLogger

settings = Settings.load_configs()

# Create default logger instance configured from settings
logger: logging.Logger = CustomLogger(name=settings.LOG_NAME, level=settings.LOG_LEVEL)._logger

__all__ = ["CustomLogger", "logger"]
