import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import DatabaseSession, RedisClient

router = APIRouter()
logger = logging.getLogger(__name__)


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


class ReadinessResponse(HealthResponse):
    checks: dict[str, Literal["ok"]]


async def database_ready(session: DatabaseSession) -> Literal["ok"]:
    try:
        result = await session.execute(text("SELECT 1"))
        if result.scalar_one() != 1:
            raise RuntimeError("Unexpected database readiness result")
    except (SQLAlchemyError, RuntimeError) as error:
        logger.warning("Database readiness check failed: %s", error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable",
        ) from error

    return "ok"


async def redis_ready(client: RedisClient) -> Literal["ok"]:
    try:
        if not await client.ping():
            raise RuntimeError("Unexpected Redis readiness result")
    except (RedisError, RuntimeError) as error:
        logger.warning("Redis readiness check failed: %s", error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis is unavailable",
        ) from error

    return "ok"


@router.get("/live", response_model=HealthResponse)
async def live() -> HealthResponse:
    return HealthResponse()


@router.get("/ready", response_model=ReadinessResponse)
async def ready(
    database: Literal["ok"] = Depends(database_ready),
    redis: Literal["ok"] = Depends(redis_ready),
) -> ReadinessResponse:
    return ReadinessResponse(
        checks={"application": "ok", "database": database, "redis": redis}
    )
