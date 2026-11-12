from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from collections.abc import Callable
from typing import Any

from fastapi import Header, HTTPException, status

JWT_SECRET = os.getenv("JWT_SECRET", "local-dev-secret")


def create_token(username: str, role: str) -> str:
    payload = {"sub": username, "role": role, "exp": int(time.time()) + 3600}
    payload_data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_b64 = base64.urlsafe_b64encode(payload_data).decode("ascii")
    signature = hmac.new(JWT_SECRET.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{signature}"


def validate_token(token: str) -> dict[str, Any]:
    if not token or "." not in token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")

    payload_b64, signature = token.split(".", 1)
    expected = hmac.new(JWT_SECRET.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature")

    try:
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "=" * (-len(payload_b64) % 4)))
    except Exception as exc:  # pragma: no cover - defensive validation
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token payload") from exc

    if int(payload.get("exp", 0)) < int(time.time()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    return payload


def require_role(allowed_roles: set[str]) -> Callable[[str | None], dict[str, Any]]:
    def dependency(authorization: str | None = Header(default=None, alias="Authorization")) -> dict[str, Any]:
        if not authorization:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")

        token = authorization.replace("Bearer ", "", 1).strip()
        claims = validate_token(token)
        if claims.get("role") not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role not permitted")
        return claims

    return dependency
