from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)
