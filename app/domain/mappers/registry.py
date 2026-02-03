from pydantic import BaseModel
from app.domain.mappers.base import BaseMapper


class MapperRegistry:
    """Simple registry for entity mappers."""

    def __init__(self) -> None:
        self._by_entity: dict[type[BaseModel], BaseMapper] = {}

    def register[
        EntityT: BaseModel,
        CreateT: BaseModel,
        UpdateT: BaseModel,
        ReadT: BaseModel,
    ](
        self,
        entity_type: type[EntityT],
        mapper: BaseMapper[EntityT, CreateT, UpdateT, ReadT],
    ) -> None:
        self._by_entity[entity_type] = mapper

    def get[
        EntityT: BaseModel,
        CreateT: BaseModel,
        UpdateT: BaseModel,
        ReadT: BaseModel,
    ](
        self,
        entity_type: type[EntityT],
    ) -> BaseMapper[EntityT, CreateT, UpdateT, ReadT]:
        mapper = self._by_entity.get(entity_type)
        if mapper is None:
            raise KeyError(f"No mapper registered for {entity_type.__name__}")
        return mapper


mapper_registry = MapperRegistry()
