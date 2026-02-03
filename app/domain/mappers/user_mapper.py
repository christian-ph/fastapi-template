from app.domain.entities.user import UserEntity
from app.domain.schemas.user import UserCreate, UserUpdate, UserRead
from app.core.security import hash_password
from app.domain.mappers.base import merge_update


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
        return UserRead(
            id=entity.id,
            email=entity.email,
            full_name=entity.full_name,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
        )
