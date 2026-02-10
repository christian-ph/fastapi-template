import logging
from pathlib import Path
from typing import Literal

import coloredlogs

from .config import get_settings


class Logger:
    """
    Enhanced logging class with colored output and multiple log levels.

    Args:
        name: Logger name (default: app name from settings)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        file_path: Optional file path for file logging
        file_level: Logging level for file output
    """

    def __init__(
        self,
        name: str | None = None,
        level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
        file_path: Path | None = None,
        file_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = None,
    ):
        settings = get_settings()
        self.name = name or settings.APP_NAME
        self.logger = logging.getLogger(self.name)

        # Set base level
        self.logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler with colors
        self._setup_console_handler(level)

        # Optional file handler
        if file_path:
            self._setup_file_handler(file_path, file_level or level)

    def _setup_console_handler(self, level: str):
        """Configure colored console logging."""
        coloredlogs.install(
            logger=self.logger,
            level=level,
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            field_styles={
                "asctime": {"color": "green"},
                "name": {"color": "blue"},
                "levelname": {"color": "magenta"},
                "message": {"color": "white"},
            },
            level_styles={
                "debug": {"color": "cyan"},
                "info": {"color": "green"},
                "warning": {"color": "yellow"},
                "error": {"color": "red"},
                "critical": {"color": "red", "bold": True},
            },
        )

    def _setup_file_handler(self, file_path: Path, level: str):
        """Configure file logging."""
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(level)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)


# Default logger instance
logger = Logger().logger
