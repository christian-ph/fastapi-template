from sqlalchemy import String, TypeDecorator, func, type_coerce
from sqlalchemy.dialects import postgresql


class EncryptedType(TypeDecorator):
    impl = String  # Tipo base por defecto
    cache_ok = True

    def __init__(self, key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            # In PostgreSQL we use BYTEA for encrypted data
            return dialect.type_descriptor(postgresql.BYTEA())
        # For other databases, fall back to String
        return dialect.type_descriptor(String())

    def bind_expression(self, bindvalue):
        # Encrypt on insert/update
        # Convert to string if needed
        bindvalue = type_coerce(bindvalue, String)
        return func.pgp_sym_encrypt(bindvalue, self.key, "cipher-algo=aes256")

    def column_expression(self, col):
        # Decrypt on select
        return func.pgp_sym_decrypt(col, self.key, "cipher-algo=aes256")
