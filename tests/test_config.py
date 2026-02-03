import os
from unittest.mock import patch

from app.infrastructure.config import Settings


def test_default_settings():
    """Test that default settings are loaded correctly."""
    # Ensure no relevant env vars are set
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings.load_configs()
        assert settings.APP_NAME == "Empty APP"
        assert settings.LOG_LEVEL == "INFO"
        assert settings.DEBUG is False
        assert settings.CORS_ORIGINS == ["*"]
        assert settings.DATABASE is not None
        assert settings.DATABASE.HOST == "localhost"


def test_env_var_override():
    """Test that environment variables override defaults."""
    env_vars = {
        "APP_NAME": "Test App",
        "DEBUG": "true",
        "PORT": "5433",  # Database port
        "POOL_SIZE": "20",
    }
    with patch.dict(os.environ, env_vars):
        settings = Settings.load_configs()
        assert settings.APP_NAME == "Test App"
        assert settings.DEBUG is True
        assert settings.DATABASE.PORT == 5433
        assert settings.DATABASE.POOL_SIZE == 20


def test_boolean_parsing():
    """Test boolean field parsing logic."""
    # Test True variations
    for val in ["true", "1", "t", "yes", "True", "TRUE"]:
        with patch.dict(os.environ, {"DEBUG": val}):
            settings = Settings.load_configs()
            assert settings.DEBUG is True, f"Failed for {val}"

    # Test False variations
    for val in ["false", "0", "f", "no", "False", "FALSE"]:
        with patch.dict(os.environ, {"DEBUG": val}):
            settings = Settings.load_configs()
            assert settings.DEBUG is False, f"Failed for {val}"


def test_list_parsing():
    """Test list field parsing logic."""
    with patch.dict(os.environ, {"CORS_ORIGINS": '["http://localhost", "https://example.com"]'}):
        settings = Settings.load_configs()
        assert settings.CORS_ORIGINS == ["http://localhost", "https://example.com"]


def test_int_parsing():
    """Test integer field parsing logic."""
    with patch.dict(os.environ, {"PORT": "9999"}):  # PORT is in DatabaseSettings
        settings = Settings.load_configs()
        assert settings.DATABASE.PORT == 9999
