from contextlib import contextmanager
from sqlalchemy.orm import Session
from app.infrastructure.config import Settings
from app.infrastructure.logging import logger
from app.infrastructure.database.connector import db_connector
from app.domain.repositories.user_repository import UserRepository as UserRepositoryInterface
from app.infrastructure.database.repositories.user_repository import UserRepository as UserRepositoryImplementation

class DependencyContainer:
    """Container for dependency management"""
    def __init__(self):
        self.settings = Settings.load_configs()
        self.logger = logger
        self._db_connector = db_connector
        
        # Repository factory
        self._repositories = self._build_repositories()

    def _build_repositories(self):
        return {
            "user_repository": UserRepositoryImplementation(
                logger=self.logger,
                settings=self.settings
            )
        }
    
    def get_db(self) -> Session:
        """Dependency that provides a database session"""
        session = self._db_connector.get_session()
        try:
            yield session
        except Exception as e:
            session.rollback()
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()
    
    def get_user_repository(self) -> UserRepositoryInterface:
        """Dependency that provides the configured user repository instance"""
        return self._repositories["user_repository"]

# FastAPI dependencies
def get_db():
    """Dependency that provides a database session"""
    yield from container.get_db()

def get_logger():
    """Dependency that provides the configured logger instance"""
    return container.logger

def get_user_repository() -> UserRepositoryInterface:
    """Dependency that provides the configured user repository instance"""
    return container.get_user_repository()

container = DependencyContainer()
