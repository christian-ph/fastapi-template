from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.domain.repositories.base_repository import CRUDRepository
from app.infrastructure.logging.base_logger import BaseLogger
from app.infrastructure.config import Settings
from typing import Type, Any, Optional, List,TypeVar

ModelType = TypeVar('ModelType')

class BaseRepositoryImpl(CRUDRepository[ModelType]):
    """
    Base repository class for CRUD operations using SQLAlchemy.
    """
    def __init__(self, model: Type[ModelType], logger: BaseLogger, settings: Settings):
        self.model = model
        self.logger = logger
        self.settings = settings
    
    def create(self, db: Session, obj: ModelType) -> ModelType:
        try:
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            self.logger.error(f"Error creating record: {str(e)}")
            raise
    
    def read(self, db: Session, id: Any) -> Optional[ModelType]:
        try:
            return db.query(self.model).get(id)
        except SQLAlchemyError as e:
            self.logger.error(f"Error reading record: {str(e)}")
            raise
    
    def read_all(self, db: Session, **filters: Any) -> List[ModelType]:
        try:
            query = db.query(self.model)
            if filters:
                query = query.filter_by(**filters)
            return query.all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error reading records: {str(e)}")
            raise
    
    def update(self, db: Session, id: Any, obj: ModelType) -> ModelType:
        try:
            db_obj = self.read(db, id)
            if not db_obj:
                raise ValueError(f"{self.model.__name__} with id {id} not found")
            values = obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()
            for key, value in values.items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            self.logger.error(f"Error updating record with id {id}: {str(e)}")
            raise
    
    def delete(self, db: Session, id: Any) -> None:
        try:
            db_obj = self.read(db, id)
            if not db_obj:
                raise ValueError(f"{self.model.__name__} with id {id} not found")
            db.delete(db_obj)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            self.logger.error(f"Error deleting record with id {id}: {str(e)}")
            raise
