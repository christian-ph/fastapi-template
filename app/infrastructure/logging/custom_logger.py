import logging
from pathlib import Path
from typing import Optional, Literal
import coloredlogs
from .base_logger import BaseLogger

class CustomLogger(BaseLogger):
    """
    Custom logging implementation with colored output and file logging support.
    Inherits from BaseLogger abstract class.
    """
    
    def __init__(
        self,
        name: str,
        level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        file_path: Optional[Path] = None,
        file_level: Optional[Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]] = None
    ):
        self._name = name
        self._level = level
        self._file_path = file_path
        self._file_level = file_level
        self._logger = None
        self._initialize_logger()
    
    def _initialize_logger(self):
        """Initialize or reinitialize the logger"""
        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(self._level)
        
        # Clear existing handlers
        self._logger.handlers.clear()
        
        # Setup console handler
        self._setup_console_handler()
        
        # Setup file handler if needed
        if self._file_path:
            self._setup_file_handler()
    
    def _setup_console_handler(self):
        """Configure colored console logging"""
        coloredlogs.install(
            logger=self._logger,
            level=self._level,
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            field_styles={
                'asctime': {'color': 'green'},
                'name': {'color': 'blue'},
                'levelname': {'color': 'magenta'},
                'message': {'color': 'white'}
            },
            level_styles={
                'debug': {'color': 'cyan'},
                'info': {'color': 'green'},
                'warning': {'color': 'yellow'},
                'error': {'color': 'red'},
                'critical': {'color': 'red', 'bold': True}
            }
        )
    
    def _setup_file_handler(self):
        """Configure file logging"""
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(self._file_path)
        file_handler.setLevel(self._file_level or self._level)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        self._logger.addHandler(file_handler)
    
    def debug(self, msg: str) -> None:
        self._logger.debug(msg)
    
    def info(self, msg: str) -> None:
        self._logger.info(msg)
    
    def warning(self, msg: str) -> None:
        self._logger.warning(msg)
    
    def error(self, msg: str) -> None:
        self._logger.error(msg)
    
    def critical(self, msg: str) -> None:
        self._logger.critical(msg)
    
    def reload(self) -> None:
        """Reload logger configuration"""
        self._initialize_logger()
    
    def reset(self) -> None:
        """Reset logger to initial state"""
        self._logger.handlers.clear()
        self._initialize_logger()
