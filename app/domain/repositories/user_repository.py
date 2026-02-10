from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import UserEntity


class UserRepository(ABC):
    """Abstract interface for user repository operations."""

    @abstractmethod
    async def create_user(self, db: AsyncSession, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def get_user_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> UserEntity | None:
        pass

    @abstractmethod
    async def get_user_by_id(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> UserEntity | None:
        pass

    @abstractmethod
    async def update_user(
        self,
        db: AsyncSession,
        user_id: int,
        user: UserEntity,
    ) -> UserEntity:
        pass

    @abstractmethod
    async def delete_user(self, db: AsyncSession, user_id: int) -> None:
        pass
