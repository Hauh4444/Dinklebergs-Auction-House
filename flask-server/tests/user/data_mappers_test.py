import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import UserMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_user(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "user_id": 1, "username": "John Doe", "email": "johndoe@example.com",
        "password_hash": "hashedpassword", "is_active": True, "created_at": datetime(2024, 1, 1), "updated_at": datetime(2025, 1, 3)
    }

    user = UserMapper.get_user(user_id=1, db_session=mock_db_session)

    assert user["user_id"] == 1
    assert user["email"] == "johndoe@example.com"


def test_update_user(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "username": "Johnny Doe",
    }

    rows_updated = UserMapper.update_user(user_id=1, data=data, db_session=mock_db_session)

    assert rows_updated == 1


def test_delete_user(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = UserMapper.delete_user(user_id=1, db_session=mock_db_session)

    assert rows_deleted == 1

def test_get_user_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        UserMapper.get_user(user_id=1, db_session=mock_db_session)


def test_update_user_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")
    updates = {
        "username": "updateduser", "email": "updateduser@example.com"
    }

    with pytest.raises(expected_exception=Exception, match="Database error"):
        UserMapper.update_user(user_id=1, data=updates, db_session=mock_db_session)


def test_delete_user_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        UserMapper.delete_user(user_id=1, db_session=mock_db_session)


def test_update_user_invalid_data(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 0  # Simulate no rows updated

    updates = {
        "username": "updateduser", "email": "updateduser@example.com"
    }

    rows_updated = UserMapper.update_user(user_id=999, data=updates, db_session=mock_db_session)  # Invalid ID

    assert rows_updated == 0  # Expecting no rows to be updated