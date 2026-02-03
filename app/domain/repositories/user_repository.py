from abc import ABC, abstractmethod
from app.domain.entities.user import UserEntity
from typing import Optional
from sqlalchemy.orm import Session

class UserRepository(ABC):
    """Abstract interface for user repository operations."""
    
    @abstractmethod
    def create_user(self, db: Session, user: UserEntity) -> UserEntity:
        pass
    
    @abstractmethod
    def get_user_by_email(self, db: Session, email: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[UserEntity]:
        pass
