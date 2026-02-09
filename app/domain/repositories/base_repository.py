from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')

class CRUDRepository(ABC, Generic[T]):
    """
    Abstract base class for CRUD operations using the Repository pattern.
    """
    
    @abstractmethod
    async def create(self, db: AsyncSession, obj: T) -> T:
        """Create a new record."""
        pass
    
    @abstractmethod
    async def read(self, db: AsyncSession, id: Any) -> Optional[T]:
        """Read a record by id."""
        pass
    
    @abstractmethod
    async def read_all(self, db: AsyncSession, **filters: Any) -> List[T]:
        """Read all records, optionally filtered."""
        pass
    
    @abstractmethod
    async def update(self, db: AsyncSession, id: Any, obj: T) -> T:
        """Update a record."""
        pass
    
    @abstractmethod
    async def delete(self, db: AsyncSession, id: Any) -> None:
        """Delete a record by id."""
        pass
