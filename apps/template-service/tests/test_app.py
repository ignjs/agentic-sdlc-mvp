from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_and_list_users() -> None:
    login = client.post("/login", json={"username": "admin", "password": "AdminPass123!"})
    assert login.status_code == 200
    token = login.json()["token"]

    response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "admin" in response.json()["users"]


def test_unauthorized_user_access() -> None:
    login = client.post("/login", json={"username": "analyst", "password": "AnalystPass123!"})
    token = login.json()["token"]

    response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
