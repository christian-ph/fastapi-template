from sqlalchemy import Column, Boolean, func
from sqlalchemy.ext.hybrid import hybrid_property
from app.infrastructure.database.types.encrypted_column import EncryptedType
from app.infrastructure.config import get_settings
from .base import Base

settings = get_settings()

class User(Base):
    __tablename__ = 'users'
    
    email = Column(EncryptedType(key=settings.SECRET_KEY), unique=True, index=True, nullable=False)
    full_name = Column(EncryptedType(key=settings.SECRET_KEY))
    
    hashed_password = Column(EncryptedType(key=settings.SECRET_KEY), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    @hybrid_property
    def decrypted_email(self):
        """Decrypted property. Only for SQL filters."""
        raise NotImplementedError("Only for SQL filters")

    @decrypted_email.expression
    def decrypted_email(cls):
        """Decrypted property. Only for SQL filters."""
        return func.pgp_sym_decrypt(cls.email, settings.SECRET_KEY, "cipher-algo=aes256")
