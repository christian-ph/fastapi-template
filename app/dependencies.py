from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.user_repository import (
    UserRepository as UserRepositoryInterface,
)
from app.infrastructure.config import Settings
from app.infrastructure.database.connector import db_connector
from app.infrastructure.database.repositories.user_repository import (
    UserRepository as UserRepositoryImplementation,
)
from app.infrastructure.logging import logger


class DependencyContainer:
    """Container for dependency management."""

    def __init__(self):
        self.settings = Settings.load_configs()
        self.logger = logger
        self._db_connector = db_connector

        # Repository factory
        self._repositories = self._build_repositories()

    def _build_repositories(self):
        return {"user_repository": UserRepositoryImplementation(logger=self.logger, settings=self.settings)}

    @asynccontextmanager
    async def get_db(self) -> AsyncIterator[AsyncSession]:
        """Dependency that provides an async database session."""
        session = self._db_connector.get_session()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            await session.close()

    def get_user_repository(self) -> UserRepositoryInterface:
        """Dependency that provides the configured user repository instance."""
        return self._repositories["user_repository"]


# FastAPI dependencies
async def get_db():
    """Dependency that provides an async database session."""
    async with container.get_db() as session:
        yield session


def get_logger():
    """Dependency that provides the configured logger instance."""
    return container.logger


def get_user_repository() -> UserRepositoryInterface:
    """Dependency that provides the configured user repository instance."""
    return container.get_user_repository()


container = DependencyContainer()
