from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Optional, List
from sqlalchemy.orm import Session

T = TypeVar('T')

class CRUDRepository(ABC, Generic[T]):
    """
    Abstract base class for CRUD operations using the Repository pattern.
    """
    
    @abstractmethod
    def create(self, db: Session, obj: T) -> T:
        """Create a new record."""
        pass
    
    @abstractmethod
    def read(self, db: Session, id: Any) -> Optional[T]:
        """Read a record by id."""
        pass
    
    @abstractmethod
    def read_all(self, db: Session, **filters: Any) -> List[T]:
        """Read all records, optionally filtered."""
        pass
    
    @abstractmethod
    def update(self, db: Session, id: Any, obj: T) -> T:
        """Update a record."""
        pass
    
    @abstractmethod
    def delete(self, db: Session, id: Any) -> None:
        """Delete a record by id."""
        pass
