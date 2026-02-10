from app.domain.entities.user import UserEntity


def test_create_user_success(client, mock_user_repo):
    """Test creating a new user successfully."""
    user_input = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "strongpassword",
    }

    expected_entity = UserEntity(
        id=1,
        email=user_input["email"],
        full_name=user_input["full_name"],
        hashed_password="hashed_secret",
        is_active=True,
        is_superuser=False,
    )
    mock_user_repo.create_user.return_value = expected_entity

    response = client.post("/api/v1/users", json=user_input)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_input["email"]
    assert data["full_name"] == user_input["full_name"]
    assert "id" in data
    assert "password" not in data

    mock_user_repo.create_user.assert_awaited_once()


def test_read_user_success(client, mock_user_repo, mock_db):
    """Test reading a user by ID successfully."""
    user_id = 99
    expected_entity = UserEntity(
        id=user_id,
        email="read@example.com",
        full_name="Reader",
        hashed_password="hash",
        is_active=True,
    )
    mock_user_repo.get_user_by_id.return_value = expected_entity

    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "read@example.com"

    mock_user_repo.get_user_by_id.assert_awaited_once_with(mock_db, user_id)


def test_read_user_not_found(client, mock_user_repo):
    """Test reading a non-existent user returns 404."""
    user_id = 999
    mock_user_repo.get_user_by_id.return_value = None

    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_read_user_by_email_success(client, mock_user_repo, mock_db):
    """Test reading a user by email successfully."""
    email = "search@example.com"
    expected_entity = UserEntity(id=5, email=email, full_name="Searcher", hashed_password="hash", is_active=True)
    mock_user_repo.get_user_by_email.return_value = expected_entity

    response = client.get(f"/api/v1/users/by-email/{email}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email

    mock_user_repo.get_user_by_email.assert_awaited_once_with(mock_db, email)


def test_update_user_success(client, mock_user_repo):
    """Test updating a user successfully."""
    user_id = 1
    update_input = {"full_name": "Updated Name"}

    existing_entity = UserEntity(
        id=user_id,
        email="original@example.com",
        full_name="Original",
        hashed_password="hash",
        is_active=True,
    )

    updated_entity = UserEntity(
        id=user_id,
        email="original@example.com",
        full_name="Updated Name",
        hashed_password="hash",
        is_active=True,
    )

    mock_user_repo.get_user_by_id.return_value = existing_entity
    mock_user_repo.update_user.return_value = updated_entity

    response = client.put(f"/api/v1/users/{user_id}", json=update_input)

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"

    mock_user_repo.update_user.assert_awaited_once()


def test_delete_user_success(client, mock_user_repo, mock_db):
    """Test deleting a user successfully."""
    user_id = 1
    existing_entity = UserEntity(id=user_id, email="d@e.com", full_name="d", hashed_password="h")
    mock_user_repo.get_user_by_id.return_value = existing_entity

    response = client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

    mock_user_repo.delete_user.assert_awaited_once_with(mock_db, user_id)
