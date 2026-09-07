from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pwdlib import PasswordHash


IDLE_LIMIT = timedelta(minutes=30)
ABSOLUTE_LIMIT = timedelta(hours=2)


@dataclass
class Session:
    token_hash: str
    user_id: str
    csrf_token: str
    created_at: datetime
    last_seen_at: datetime
    expires_at: datetime
    revoked: bool = False


class IdentityService:
    def __init__(self, users: list[dict], demo_password: str, now=lambda: datetime.now(timezone.utc)):
        self.users = {u["id"]: {**u, "account_state": "active"} for u in users}
        self.by_email = {u["email"].casefold(): u["id"] for u in users}
        self.password_hash = PasswordHash.recommended()
        self.demo_hash = self.password_hash.hash(demo_password)
        self.now = now
        self.sessions: dict[str, Session] = {}

    @classmethod
    def from_synthetic_data(cls, demo_password: str, now=lambda: datetime.now(timezone.utc)):
        path = Path(__file__).resolve().parents[2] / "data" / "synthetic" / "source" / "users.json"
        import json
        return cls(json.loads(path.read_text(encoding="utf-8")), demo_password, now)

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def authenticate(self, email: str, password: str) -> tuple[str, dict] | None:
        user_id = self.by_email.get(email.casefold())
        valid = self.password_hash.verify(password, self.demo_hash)
        user = self.users.get(user_id) if user_id else None
        if not valid or not user or user["account_state"] != "active":
            return None
        now = self.now()
        token = secrets.token_urlsafe(32)
        session = Session(
            token_hash=self._hash_token(token),
            user_id=user_id,
            csrf_token=secrets.token_urlsafe(24),
            created_at=now,
            last_seen_at=now,
            expires_at=now + ABSOLUTE_LIMIT,
        )
        self.sessions[session.token_hash] = session
        return token, self.public_context(user_id) | {"csrf_token": session.csrf_token}

    def resolve(self, token: str | None, touch: bool = True) -> tuple[Session, dict] | None:
        if not token:
            return None
        session = self.sessions.get(self._hash_token(token))
        if not session or session.revoked:
            return None
        now = self.now()
        user = self.users.get(session.user_id)
        if (
            not user
            or user["account_state"] != "active"
            or now >= session.expires_at
            or now - session.last_seen_at >= IDLE_LIMIT
        ):
            session.revoked = True
            return None
        if touch:
            session.last_seen_at = now
        return session, user

    def revoke(self, token: str) -> None:
        session = self.sessions.get(self._hash_token(token))
        if session:
            session.revoked = True

    def public_context(self, user_id: str) -> dict:
        user = self.users[user_id]
        return {key: user[key] for key in (
            "id", "display_name", "email", "role", "department_id",
            "primary_site_id", "site_scope",
        )}
