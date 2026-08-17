from collections.abc import Generator
from typing import Literal

import pytest
from fastapi.testclient import TestClient

from app.api.v1.routes.health import database_ready, redis_ready
from app.main import app


async def database_ready_override() -> Literal["ok"]:
    return "ok"


async def redis_ready_override() -> Literal["ok"]:
    return "ok"


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[database_ready] = database_ready_override
    app.dependency_overrides[redis_ready] = redis_ready_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
