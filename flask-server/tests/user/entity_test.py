import pytest
from datetime import datetime
from app.entities import User

def test_user_creation():
    user = User(
        user_id=1,
        username="testuser",
        password_hash="hashedpassword",
        email="test@example.com",
        is_active=True
    )
    
    assert user.user_id == 1
    assert user.username == "testuser"
    assert user.password_hash == "hashedpassword"
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    assert isinstance(user.last_login, datetime)

def test_user_with_optional_fields():
    user = User(
        user_id=2,
        username="janedoe",
        password_hash="securehash",
        email="jane@example.com",
        is_active=False,
        created_at=datetime(2024, 3, 18, 10, 0, 0),
        updated_at=datetime(2024, 3, 18, 12, 0, 0),
        last_login=datetime(2024, 3, 17, 9, 30, 0)
    )
    
    assert user.created_at == datetime(2024, 3, 18, 10, 0, 0)
    assert user.updated_at == datetime(2024, 3, 18, 12, 0, 0)
    assert user.last_login == datetime(2024, 3, 17, 9, 30, 0)
    assert user.is_active is False

def test_user_to_dict():
    user = User(
        user_id=3,
        username="alice123",
        password_hash="alicehash",
        email="alice@example.com",
        is_active=True
    )
    
    user_dict = user.to_dict()
    
    assert user_dict["user_id"] == 3
    assert user_dict["username"] == "alice123"
    assert user_dict["password_hash"] == "alicehash"
    assert user_dict["email"] == "alice@example.com"
    assert user_dict["is_active"] is True

def test_user_missing_required_fields():
    with pytest.raises(TypeError):
        User()

def test_user_invalid_types():
    with pytest.raises(TypeError):
        User(
            user_id="1",
            username=123,
            password_hash=456,
            email=789,
            is_active="True"
        )

def test_user_invalid_username_length():
    with pytest.raises(ValueError):
        user = User(
            user_id=4,
            username="ab",
            password_hash="shortname",
            email="short@example.com",
            is_active=True
        )
