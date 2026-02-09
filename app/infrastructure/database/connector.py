from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.infrastructure.config import Settings
from app.infrastructure.database.models import Base, create_schema
from urllib.parse import quote_plus

class DatabaseConnector:
    """
    SQLAlchemy database connector with connection management, session handling,
    and URI generation from settings.
    """
    
    def __init__(self, settings: Settings, logger):
        self.settings = settings
        self._logger = logger
        self._engine = None
        self._session_factory = None
    
    @property
    def database_uri(self) -> str:
        """Generate database URI with escaped credentials"""
        escaped_user = quote_plus(self.settings.DATABASE.DB_USER)
        escaped_password = quote_plus(self.settings.DATABASE.DB_PASSWORD)
        uri = (
            f"postgresql+psycopg://{escaped_user}:{escaped_password}@"
            f"{self.settings.DATABASE.HOST}:{self.settings.DATABASE.PORT}/"
            f"{self.settings.DATABASE.DB_NAME}"
        )
        self._logger.debug("Database URI generated: %s", uri)
        return uri
    
    def create_engine(self):
        """Create SQLAlchemy async engine using escaped URI."""
        if self._engine is None:
            self._logger.info("Creating database engine")
            self._engine = create_async_engine(
                self.database_uri,
                pool_pre_ping=True,
                echo=self.settings.ENVIRONMENT == "DEV",
            )
        return self._engine
    
    def create_session_factory(self):
        """Create async session factory."""
        if self._session_factory is None:
            engine = self.create_engine()
            self._session_factory = async_sessionmaker(
                bind=engine,
                autoflush=False,
                expire_on_commit=False,
                class_=AsyncSession,
            )
        return self._session_factory
    
    def get_session(self) -> AsyncSession:
        """Get a new async database session."""
        session_factory = self.create_session_factory()
        return session_factory()
    
    async def create_database(self):
        """Create all database tables."""
        try:
            engine = self.create_engine()
            async with engine.begin() as conn:
                await conn.run_sync(create_schema)
                await conn.run_sync(Base.metadata.create_all)
            self._logger.info("Database tables created in schema %s", self.settings.DATABASE.DB_SCHEMA)
        except SQLAlchemyError as e:
            self._logger.error(f"Error creating database: {e}")
            raise
    
    async def drop_database(self):
        """Drop all database tables."""
        try:
            engine = self.create_engine()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            self._logger.warning("Database tables dropped from schema %s", self.settings.DATABASE.DB_SCHEMA)
        except SQLAlchemyError as e:
            self._logger.error(f"Error dropping database: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if database is reachable."""
        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as e:
            self._logger.error(f"Database health check failed: {e}")
            return False

# Singleton instance
from app.infrastructure.logging import logger
db_connector = DatabaseConnector(Settings.load_configs(), logger)
