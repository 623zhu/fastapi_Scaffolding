from fastapi.testclient import TestClient


def test_liveness(client: TestClient) -> None:
    response = client.get("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness(client: TestClient) -> None:
    response = client.get("/api/v1/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "checks": {"application": "ok", "database": "ok", "redis": "ok"},
    }


def test_openapi_document(client: TestClient) -> None:
    response = client.get("/api/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "FastAPI Vue Starter"
    assert "/api/v1/users" in response.json()["paths"]

    response_schema = response.json()["components"]["schemas"]["UserRead"]
    assert "password_hash" not in response_schema["properties"]
