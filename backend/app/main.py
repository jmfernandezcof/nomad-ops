from __future__ import annotations

import os

from fastapi import Cookie, Depends, FastAPI, Header, HTTPException, Path, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from starlette.middleware.trustedhost import TrustedHostMiddleware

from simulator import SimulationService

from .policy import PolicyEngine
from .security import IdentityService


COOKIE = "nomad_session"


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)


def create_app(identity: IdentityService | None = None, simulator: SimulationService | None = None) -> FastAPI:
    if identity is None:
        password = os.environ.get("NOMAD_DEMO_PASSWORD")
        if not password:
            raise RuntimeError("NOMAD_DEMO_PASSWORD is required")
        identity = IdentityService.from_synthetic_data(password)
    simulator = simulator or SimulationService()
    policy = PolicyEngine()
    production = os.environ.get("NOMAD_ENV", "development").casefold() == "production"
    configured_hosts = os.environ.get("NOMAD_ALLOWED_HOSTS")
    allowed_hosts = [
        host.strip()
        for host in (configured_hosts or "localhost,127.0.0.1,testserver").split(",")
        if host.strip()
    ]
    if production and (configured_hosts is None or not allowed_hosts or "*" in allowed_hosts):
        raise RuntimeError("NOMAD_ALLOWED_HOSTS must be an explicit production allowlist")
    cookie_secure = production or os.environ.get("NOMAD_COOKIE_SECURE", "true").casefold() == "true"

    app = FastAPI(
        title="NOMAD Ops",
        version="0.1.0",
        docs_url=None if production else "/docs",
        redoc_url=None if production else "/redoc",
        openapi_url=None if production else "/openapi.json",
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

    @app.middleware("http")
    async def api_security_headers(request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
            response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
            response.headers["Permissions-Policy"] = "camera=(), geolocation=(), microphone=()"
            response.headers["Referrer-Policy"] = "no-referrer"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
        return response

    def current(nomad_session: str | None = Cookie(default=None, alias=COOKIE)):
        resolved = identity.resolve(nomad_session)
        if not resolved:
            raise HTTPException(401, "Authentication required")
        return nomad_session, resolved[0], resolved[1]

    @app.get("/api/v1/health")
    def health():
        return {"status": "healthy", "service": "nomad-ops"}

    @app.post("/api/v1/auth/login")
    def login(payload: LoginRequest, response: Response):
        authenticated = identity.authenticate(payload.email, payload.password)
        if not authenticated:
            raise HTTPException(401, "Invalid credentials")
        token, context = authenticated
        response.set_cookie(
            COOKIE, token, httponly=True, secure=cookie_secure,
            samesite="strict", max_age=7200, path="/",
        )
        return {"user": {k: v for k, v in context.items() if k != "csrf_token"}, "csrf_token": context["csrf_token"]}

    @app.post("/api/v1/auth/logout")
    def logout(
        response: Response,
        auth=Depends(current),
        x_csrf_token: str | None = Header(default=None),
    ):
        token, session, _ = auth
        if not x_csrf_token or not secrets_compare(x_csrf_token, session.csrf_token):
            raise HTTPException(403, "Invalid request protection token")
        identity.revoke(token)
        response.delete_cookie(COOKIE, path="/")
        return {"status": "logged_out"}

    @app.get("/api/v1/auth/me")
    def me(auth=Depends(current)):
        return {
            "user": identity.public_context(auth[2]["id"]),
            "csrf_token": auth[1].csrf_token,
        }

    @app.get("/api/v1/documents/search")
    def search_documents(q: str = Query(default="", max_length=200), auth=Depends(current)):
        user = auth[2]
        if policy.decide(user, "documents.search").outcome != "ALLOW":
            raise HTTPException(403, "Access denied")
        return simulator.call(sim_request(user, "documents.search_documents", query=q))

    @app.get("/api/v1/alerts/{alert_id}")
    def get_alert(
        alert_id: str = Path(min_length=7, max_length=32, pattern=r"^ALT-[A-Z0-9-]+$"),
        auth=Depends(current),
    ):
        user = auth[2]
        if policy.decide(user, "alerts.read").outcome != "ALLOW":
            raise HTTPException(403, "Access denied")
        return simulator.call(sim_request(user, "monitoring.get_alert", record_id=alert_id))

    return app


def secrets_compare(left: str, right: str) -> bool:
    import secrets
    return secrets.compare_digest(left, right)


def sim_request(user: dict, operation: str, **values) -> dict:
    import secrets
    return {
        "request_id": secrets.token_urlsafe(12),
        "caller_service_id": "nomad-ops-svc",
        "actor_id": user["id"],
        "actor_context": {
            "role": user["role"],
            "department_id": user["department_id"],
            "site_scope": user["site_scope"],
        },
        "operation": operation,
        **values,
    }


if os.environ.get("NOMAD_DEMO_PASSWORD"):
    app = create_app()
