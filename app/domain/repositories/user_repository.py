from abc import ABC, abstractmethod
from app.domain.entities.user import UserEntity
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(ABC):
    """Abstract interface for user repository operations."""
    
    @abstractmethod
    async def create_user(self, db: AsyncSession, user: UserEntity) -> UserEntity:
        pass
    
    @abstractmethod
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> Optional[UserEntity]:
        pass
