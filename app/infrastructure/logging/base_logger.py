from abc import ABC, abstractmethod


class BaseLogger(ABC):
    """
    Abstract base class for all logger implementations.
    """

    @abstractmethod
    def debug(self, msg: str) -> None:
        pass

    @abstractmethod
    def info(self, msg: str) -> None:
        pass

    @abstractmethod
    def warning(self, msg: str) -> None:
        pass

    @abstractmethod
    def error(self, msg: str) -> None:
        pass

    @abstractmethod
    def critical(self, msg: str) -> None:
        pass

    @abstractmethod
    def reload(self) -> None:
        """Reload logger configuration"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset logger to initial state"""
        pass
