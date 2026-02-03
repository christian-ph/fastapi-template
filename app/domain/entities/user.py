from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserEntity(BaseModel):
    id: Optional[int] = None
    email: str
    full_name: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    model_config = ConfigDict(from_attributes=True)
