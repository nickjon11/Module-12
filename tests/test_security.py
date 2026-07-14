import pytest

from app.security import hash_password, verify_password


def test_hash_password_is_not_plain_text():
    password = "SecurePassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert password not in hashed


def test_verify_password_accepts_correct_password():
    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_rejects_incorrect_password():
    hashed = hash_password("SecurePassword123!")

    assert verify_password("WrongPassword123!", hashed) is False


def test_same_password_creates_different_hashes():
    password = "SecurePassword123!"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash


def test_empty_password_raises_error():
    with pytest.raises(ValueError):
        hash_password("")
