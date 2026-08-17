from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserAlreadyExistsError(Exception):
    pass


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = UserRepository(session)

    async def register(self, data: UserCreate) -> User:
        email = str(data.email).lower()
        existing_user = await self.repository.get_by_username_or_email(data.username, email)
        if existing_user is not None:
            raise UserAlreadyExistsError

        try:
            user = await self.repository.add(
                username=data.username,
                email=email,
                password_hash=hash_password(data.password.get_secret_value()),
            )
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            raise UserAlreadyExistsError from error

        await self.session.refresh(user)
        return user
