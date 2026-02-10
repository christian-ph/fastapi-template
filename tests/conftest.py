from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_db, get_user_repository
from app.infrastructure.config import DatabaseSettings, Settings, get_settings
from app.infrastructure.database.connector import DatabaseConnector
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.main import app


@pytest.fixture(autouse=True)
def clean_env():
    """
    Ensure a clean configuration environment for each test.
    Patches load_dotenv and Pydantic model_config to prevent reading real .env files.
    """
    with patch("app.infrastructure.config.load_dotenv"), patch("app.infrastructure.config.print"):
        # Store original configs
        original_settings_config = Settings.model_config.copy()
        original_db_config = DatabaseSettings.model_config.copy()

        # Disable env_file reading
        Settings.model_config["env_file"] = None
        DatabaseSettings.model_config["env_file"] = None

        with patch.object(DatabaseConnector, "create_database", new=AsyncMock()):
            get_settings.cache_clear()
            yield

        # Restore original configs
        Settings.model_config = original_settings_config
        DatabaseSettings.model_config = original_db_config
        get_settings.cache_clear()


@pytest.fixture
def mock_db():
    """Fixture for a mocked database session."""
    return MagicMock()


@pytest.fixture
def mock_user_repo():
    """Fixture for a mocked user repository."""
    repo = MagicMock(spec=UserRepository)
    repo.create_user = AsyncMock()
    repo.get_user_by_id = AsyncMock()
    repo.get_user_by_email = AsyncMock()
    repo.update_user = AsyncMock()
    repo.delete_user = AsyncMock()
    return repo


@pytest.fixture
def client(mock_user_repo, mock_db):
    """
    Fixture for a FastAPI TestClient with dependency overrides.
    Automatically handles repo and db mocking.
    """

    # Apply overrides
    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_user_repository] = lambda: mock_user_repo
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clear overrides after test
    app.dependency_overrides.clear()
