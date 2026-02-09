from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import UserEntity
from app.domain.repositories.user_repository import UserRepository as UserRepositoryInterface
from app.infrastructure.database.models.user import User as UserModel
from app.infrastructure.database.repositories.base_repository_impl import BaseRepositoryImpl
from typing import Optional
from app.infrastructure.logging.base_logger import BaseLogger
from app.infrastructure.config import Settings


class UserRepository(BaseRepositoryImpl[UserModel], UserRepositoryInterface):
    """
    Repository class for User operations.
    """
    def __init__(self, logger: BaseLogger, settings: Settings):
        super().__init__(UserModel, logger, settings)
    
    async def create_user(self, db: AsyncSession, user: UserEntity) -> UserEntity:
        """Create a new user."""
        db_user = self._to_model(user)
        created_user = await self.create(db, db_user)
        return self._to_entity(created_user)
    
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[UserEntity]:
        """Get a user by email."""
        stmt = select(UserModel).where(UserModel.decrypted_email == email)
        result = await db.execute(stmt)
        db_user = result.scalars().first()
        if db_user is None:
            return None
        return self._to_entity(db_user)
    
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> Optional[UserEntity]:
        """Get a user by ID."""
        db_user = await self.read(db, user_id)
        if db_user is None:
            return None
        return self._to_entity(db_user)
    
    def _to_entity(self, model: UserModel) -> UserEntity:
        """Convert database model to domain entity."""
        return UserEntity(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            is_superuser=model.is_superuser,
        )
    
    def _to_model(self, entity: UserEntity) -> UserModel:
        """Convert domain entity to database model."""
        return UserModel(
            id=entity.id,
            email=entity.email,
            full_name=entity.full_name,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
        )
