from app.core.security import hash_password, verify_password


def test_password_is_hashed_and_verifiable() -> None:
    plain_password = "correct-horse-battery-staple"

    hashed_password = hash_password(plain_password)

    assert hashed_password != plain_password
    assert verify_password(plain_password, hashed_password)
    assert not verify_password("wrong-password", hashed_password)
