from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.base_repository import CRUDRepository
from app.infrastructure.config import Settings
from app.infrastructure.logging.base_logger import BaseLogger

ModelType = TypeVar("ModelType")


class BaseRepositoryImpl(CRUDRepository[ModelType]):
    """
    Base repository class for CRUD operations using SQLAlchemy.
    """

    def __init__(self, model: type[ModelType], logger: BaseLogger, settings: Settings):
        self.model = model
        self.logger = logger
        self.settings = settings

    async def create(self, db: AsyncSession, obj: ModelType) -> ModelType:
        try:
            db.add(obj)
            await db.commit()
            await db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            await db.rollback()
            self.logger.error(f"Error creating record: {str(e)}")
            raise

    async def read(self, db: AsyncSession, id: Any) -> ModelType | None:
        try:
            return await db.get(self.model, id)
        except SQLAlchemyError as e:
            self.logger.error(f"Error reading record: {str(e)}")
            raise

    async def read_all(self, db: AsyncSession, **filters: Any) -> list[ModelType]:
        try:
            stmt = select(self.model)
            if filters:
                stmt = stmt.filter_by(**filters)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            self.logger.error(f"Error reading records: {str(e)}")
            raise

    async def update(self, db: AsyncSession, id: Any, obj: ModelType) -> ModelType:
        try:
            db_obj = await self.read(db, id)
            if not db_obj:
                raise ValueError(f"{self.model.__name__} with id {id} not found")
            values = obj.model_dump() if hasattr(obj, "model_dump") else obj.__dict__
            for key, value in values.items():
                setattr(db_obj, key, value)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await db.rollback()
            self.logger.error(f"Error updating record with id {id}: {str(e)}")
            raise

    async def delete(self, db: AsyncSession, id: Any) -> None:
        try:
            db_obj = await self.read(db, id)
            if not db_obj:
                raise ValueError(f"{self.model.__name__} with id {id} not found")
            await db.delete(db_obj)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            self.logger.error(f"Error deleting record with id {id}: {str(e)}")
            raise
