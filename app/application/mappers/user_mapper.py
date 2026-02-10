from app.application.dto.user import UserCreate, UserRead, UserUpdate
from app.application.mappers.base import merge_update
from app.domain.entities.user import UserEntity
from app.infrastructure.security import hash_password


class UserMapper:
    @staticmethod
    def create_to_entity(user_create: UserCreate) -> UserEntity:
        return UserEntity(
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hash_password(user_create.password),
        )

    @staticmethod
    def update_to_entity(user_update: UserUpdate, current: UserEntity) -> UserEntity:
        merged = merge_update(
            current,
            user_update,
            field_map={"password": "hashed_password"},
            transforms={"password": hash_password},
        )
        return UserEntity(**merged)

    @staticmethod
    def to_read(entity: UserEntity) -> UserRead:
        if entity.id is None:
            raise ValueError("UserEntity.id is required for UserRead")
        return UserRead(
            id=entity.id,
            email=entity.email,
            full_name=entity.full_name,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
        )
