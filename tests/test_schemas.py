import pytest
from pydantic import ValidationError

from app.schemas import UserCreate


def test_valid_user_schema():
    user = UserCreate(
        username="jonathan",
        email="jonathan@example.com",
        password="SecurePassword123!",
    )

    assert user.username == "jonathan"
    assert str(user.email) == "jonathan@example.com"


def test_invalid_email_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(
            username="jonathan",
            email="not-an-email",
            password="SecurePassword123!",
        )


def test_short_password_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(
            username="jonathan",
            email="jonathan@example.com",
            password="short",
        )


def test_short_username_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(
            username="jo",
            email="jonathan@example.com",
            password="SecurePassword123!",
        )


def test_invalid_username_characters_are_rejected():
    with pytest.raises(ValidationError):
        UserCreate(
            username="jonathan smith",
            email="jonathan@example.com",
            password="SecurePassword123!",
        )
