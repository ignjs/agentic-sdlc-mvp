from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field, field_validator

from app.core.security import create_token, require_role

app = FastAPI(title="Secure Document API", version="0.1.0")

USER_DB = {
    "admin": {"password": "AdminPass123!", "role": "admin"},
    "analyst": {"password": "AnalystPass123!", "role": "analyst"},
}


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if any(char.isspace() for char in value):
            raise ValueError("Username cannot contain spaces")
        return value


class DocumentPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    size_bytes: int = Field(..., gt=0, le=10_000_000)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if value.startswith("/") or ".." in value:
            raise ValueError("Invalid document name")
        return value


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/login")
def login(payload: LoginRequest) -> dict[str, str]:
    user = USER_DB.get(payload.username)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_token(payload.username, user["role"])
    return {"token": token, "role": user["role"]}


@app.get("/users")
def list_users(_: str = Depends(require_role({"admin"}))) -> dict[str, list[str]]:
    return {"users": sorted(USER_DB.keys())}


@app.post("/documents")
def upload_document(
    payload: DocumentPayload,
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> dict[str, str]:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")

    claims = require_role({"admin", "analyst"})(authorization)
    if claims["role"] not in {"admin", "analyst"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return {
        "message": "Document accepted",
        "document_name": payload.name,
        "size_bytes": str(payload.size_bytes),
        "actor": claims["sub"],
    }
