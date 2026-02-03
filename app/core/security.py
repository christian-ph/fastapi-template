import hashlib


def hash_password(password: str) -> str:
    # Simple hash for template use; replace with a stronger algorithm in production.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
