from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from backend.app.main import COOKIE, create_app
from backend.app.security import IdentityService
from simulator import SimulationService


PASSWORD = "correct horse demo battery"


class Clock:
    def __init__(self):
        self.value = datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.value


def make_client():
    clock = Clock()
    identity = IdentityService.from_synthetic_data(PASSWORD, clock)
    return TestClient(create_app(identity, SimulationService()), base_url="https://testserver"), identity, clock


def login(client, user=6):
    return client.post("/api/v1/auth/login", json={
        "email": f"user{user:03d}@asteria.example", "password": PASSWORD,
    })


def test_health_and_generic_bad_login():
    client, _, _ = make_client()
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.headers["cache-control"] == "no-store"
    assert health.headers["x-content-type-options"] == "nosniff"
    response = client.post("/api/v1/auth/login", json={
        "email": "missing@asteria.example", "password": "wrong",
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_me_logout_and_cookie_security():
    client, _, _ = make_client()
    response = login(client)
    assert response.status_code == 200
    assert "HttpOnly" in response.headers["set-cookie"]
    assert "SameSite=strict" in response.headers["set-cookie"]
    csrf = response.json()["csrf_token"]
    current = client.get("/api/v1/auth/me").json()
    assert current["user"]["id"] == "USR-006"
    assert current["csrf_token"] == csrf
    assert client.post("/api/v1/auth/logout").status_code == 403
    assert client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": csrf}).status_code == 200
    assert client.get("/api/v1/auth/me").status_code == 401


def test_idle_and_absolute_session_expiry():
    client, _, clock = make_client()
    login(client)
    clock.value += timedelta(minutes=30)
    assert client.get("/api/v1/auth/me").status_code == 401

    client, _, clock = make_client()
    login(client)
    for _ in range(3):
        clock.value += timedelta(minutes=29)
        assert client.get("/api/v1/auth/me").status_code == 200
    clock.value += timedelta(minutes=33)
    assert client.get("/api/v1/auth/me").status_code == 401


def test_authorized_document_and_cross_site_alert():
    client, _, _ = make_client()
    login(client, 6)
    docs = client.get("/api/v1/documents/search?q=supplier%20onboarding").json()
    assert [item["id"] for item in docs["data"]] == ["DOC-001"]

    client, _, _ = make_client()
    login(client, 1)
    assert client.get("/api/v1/alerts/ALT-003").json()["outcome"] == "SUCCESS"
    assert client.get("/api/v1/alerts/ALT-004").json()["outcome"] == "DENIED"


def test_employee_cannot_use_alert_capability():
    client, _, _ = make_client()
    login(client, 6)
    assert client.get("/api/v1/alerts/ALT-003").status_code == 403


def test_request_validation_rejects_extra_and_oversized_input():
    client, _, _ = make_client()
    extra = client.post("/api/v1/auth/login", json={
        "email": "user006@asteria.example", "password": PASSWORD, "role": "admin",
    })
    assert extra.status_code == 422
    login(client)
    assert client.get("/api/v1/documents/search", params={"q": "x" * 201}).status_code == 422
    assert client.get("/api/v1/alerts/not-an-alert").status_code == 422


def test_production_requires_hosts_and_disables_api_docs(monkeypatch):
    monkeypatch.setenv("NOMAD_ENV", "production")
    monkeypatch.delenv("NOMAD_ALLOWED_HOSTS", raising=False)
    identity = IdentityService.from_synthetic_data(PASSWORD)
    try:
        create_app(identity, SimulationService())
    except RuntimeError as error:
        assert str(error) == "NOMAD_ALLOWED_HOSTS must be an explicit production allowlist"
    else:
        raise AssertionError("production must require an explicit host allowlist")

    monkeypatch.setenv("NOMAD_ALLOWED_HOSTS", "portfolio.example")
    monkeypatch.setenv("NOMAD_COOKIE_SECURE", "false")
    app = create_app(identity, SimulationService())
    client = TestClient(app, base_url="https://portfolio.example")
    assert client.get("/docs").status_code == 404
    assert client.get("/openapi.json").status_code == 404
    assert "Secure" in login(client).headers["set-cookie"]
    assert TestClient(app, base_url="https://attacker.example").get("/api/v1/health").status_code == 400

    monkeypatch.setenv("NOMAD_ALLOWED_HOSTS", "*")
    try:
        create_app(identity, SimulationService())
    except RuntimeError as error:
        assert "explicit production allowlist" in str(error)
    else:
        raise AssertionError("production must reject wildcard hosts")
