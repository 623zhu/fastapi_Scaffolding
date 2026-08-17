import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


def test_user_registration_schema_accepts_email() -> None:
    user = UserCreate(
        username="alice",
        email="Alice@Example.COM",
        password="correct-horse-battery-staple",
    )

    assert user.username == "alice"
    assert str(user.email) == "Alice@example.com"


@pytest.mark.parametrize("email", ["invalid", "missing-at.example.com", "@example.com"])
def test_user_registration_schema_rejects_invalid_email(email: str) -> None:
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email=email, password="valid-password")
