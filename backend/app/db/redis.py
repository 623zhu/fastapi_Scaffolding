from redis.asyncio import Redis

from app.core.config import get_settings

settings = get_settings()

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    password=(
        settings.redis_password.get_secret_value() if settings.redis_password is not None else None
    ),
    decode_responses=True,
    health_check_interval=30,
)


async def close_redis() -> None:
    await redis_client.aclose()
