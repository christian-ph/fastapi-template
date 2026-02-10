from collections.abc import Callable
from typing import Any, Protocol

from pydantic import BaseModel

type TransformFn = Callable[[Any], Any]


class BaseMapper[
    EntityT: BaseModel,
    CreateT: BaseModel,
    UpdateT: BaseModel,
    ReadT: BaseModel,
](Protocol):
    """Protocol for mapper implementations."""

    def create_to_entity(self, create_dto: CreateT) -> EntityT: ...

    def update_to_entity(self, update_dto: UpdateT, current: EntityT) -> EntityT: ...

    def to_read(self, entity: EntityT) -> ReadT: ...


def merge_update[
    CurrentT: BaseModel,
    UpdateT: BaseModel,
](
    current: CurrentT,
    update: UpdateT,
    *,
    field_map: dict[str, str] | None = None,
    transforms: dict[str, TransformFn] | None = None,
) -> dict[str, Any]:
    """
    Merge an update DTO into an existing model using model_dump.

    - field_map maps input field names to target field names.
    - transforms applies per-field transformations before merging.
    """
    field_map = field_map or {}
    transforms = transforms or {}

    update_data = update.model_dump(exclude_unset=True)
    normalized: dict[str, Any] = {}

    for key, value in update_data.items():
        target_key = field_map.get(key, key)
        transform = transforms.get(key)
        normalized[target_key] = transform(value) if transform else value

    base_data = current.model_dump()
    base_data.update(normalized)
    return base_data
