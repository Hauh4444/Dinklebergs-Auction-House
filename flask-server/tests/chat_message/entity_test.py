import pytest
from unittest.mock import MagicMock

from datetime import datetime

from app.entities.chat_message import ChatMessage


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_chat_message_creation():
    chat_message = ChatMessage(
        sender_id=1,
        chat_id=1,
        message="hello",
    )

    assert chat_message.sender_id == 1
    assert chat_message.chat_id == 1
    assert isinstance(chat_message.message, str)


def test_chat_message_with_optional_fields():
    chat_message = ChatMessage(
        message_id=1,
        sender_id=1,
        chat_id=1,
        message="hello",
        sent_at=datetime(2024, 1, 1, 10, 0, 0),
    )

    assert chat_message.message_id == 1
    assert chat_message.sender_id == 1
    assert chat_message.chat_id == 1
    assert chat_message.message == "hello"
    assert chat_message.sent_at == datetime(2024, 1, 1, 10, 0, 0)


def test_chat_message_to_dict():
    chat_message = ChatMessage(
        sender_id=1,
        chat_id=1,
        message="hello",
    )

    chat_message_dict = chat_message.to_dict()

    assert chat_message_dict["sender_id"] == 1
    assert chat_message_dict["chat_id"] == 1
    assert isinstance(chat_message_dict["message"], str)


def test_chat_message_missing_required_fields():
    with pytest.raises(expected_exception=TypeError):
        ChatMessage()


def test_chat_message_invalid_types():
    with pytest.raises(expected_exception=TypeError):
        ChatMessage(sender_id="1", chat_id="2")