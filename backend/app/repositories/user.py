from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_username_or_email(self, username: str, email: str) -> User | None:
        statement = select(User).where(or_(User.username == username, User.email == email))
        return await self.session.scalar(statement)

    async def add(self, *, username: str, email: str, password_hash: str) -> User:
        user = User(username=username, email=email, password_hash=password_hash)
        self.session.add(user)
        await self.session.flush()
        return user
