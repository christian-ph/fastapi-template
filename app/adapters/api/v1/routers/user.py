from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user import UserCreate, UserRead, UserUpdate
from app.application.mappers.user_mapper import UserMapper
from app.dependencies import get_db, get_user_repository
from app.infrastructure.database.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/test")
async def test_db_operations(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Test endpoint for database operations."""
    try:
        # Create test user
        test_input = UserCreate(
            email="test@example.com",
            full_name="Test User",
            password="fakepassword",
        )
        test_user = UserMapper.create_to_entity(test_input)
        await repository.create_user(db, test_user)

        # Query users
        result = await db.execute(select(repository.model))
        users = result.scalars().all()

        return {
            "message": "Database test completed",
            "users_count": len(users),
            "users": [{"email": u.email, "full_name": u.full_name} for u in users],
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("", response_model=UserRead)
async def create_user(
    user: UserCreate,
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        entity = UserMapper.create_to_entity(user)
        db_user = await repository.create_user(db, entity)
        return UserMapper.to_read(db_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    db_user = await repository.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserMapper.to_read(db_user)


@router.get("/by-email/{email}", response_model=UserRead)
async def read_user_by_email(
    email: str,
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    db_user = await repository.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserMapper.to_read(db_user)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user: UserUpdate,
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    current = await repository.get_user_by_id(db, user_id)
    if not current:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        entity = UserMapper.update_to_entity(user, current)
        updated_user = await repository.update_user(db, user_id, entity)
        return UserMapper.to_read(updated_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    db_user = await repository.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        await repository.delete_user(db, user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
