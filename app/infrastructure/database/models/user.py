from sqlalchemy import Boolean, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.config import get_settings
from app.infrastructure.database.types.encrypted_column import EncryptedType

from .base import Base

settings = get_settings()


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        EncryptedType(key=settings.SECRET_KEY),
        unique=True,
        index=True,
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(EncryptedType(key=settings.SECRET_KEY))

    hashed_password: Mapped[str] = mapped_column(
        EncryptedType(key=settings.SECRET_KEY),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    @hybrid_property
    def decrypted_email(self) -> str:
        """Decrypted property. Only for SQL filters."""
        raise NotImplementedError("Only for SQL filters")

    @decrypted_email.expression  # type: ignore[no-redef]
    def decrypted_email(cls) -> str:
        """Decrypted property. Only for SQL filters."""
        return func.pgp_sym_decrypt(cls.email, settings.SECRET_KEY, "cipher-algo=aes256")
