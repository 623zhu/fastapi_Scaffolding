from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import redis_client
from app.db.session import session_factory


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


DatabaseSession = Annotated[AsyncSession, Depends(get_db_session)]


def get_redis_client() -> Redis:
    return redis_client


RedisClient = Annotated[Redis, Depends(get_redis_client)]
