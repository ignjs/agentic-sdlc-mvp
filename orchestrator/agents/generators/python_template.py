from __future__ import annotations

from pathlib import Path

from orchestrator.agents.generators.common import write_if_missing


def scaffold_python_microservice(project_root: Path) -> None:
    service_root = project_root / "apps" / "template-service"

    write_if_missing(service_root / "app" / "__init__.py", "")
    write_if_missing(service_root / "app" / "core" / "__init__.py", "")

    write_if_missing(
        service_root / "app" / "core" / "security.py",
        """from __future__ import annotations

from fastapi import Header, HTTPException


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key != "dev-local-key":
        raise HTTPException(status_code=401, detail="Invalid API key")
""",
    )

    write_if_missing(
        service_root / "app" / "main.py",
        """from __future__ import annotations

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from app.core.security import verify_api_key

app = FastAPI(title="Template Secure Service", version="0.1.0")


class EchoRequest(BaseModel):
    message: str = Field(min_length=1, max_length=256)


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/echo", dependencies=[Depends(verify_api_key)])
def secure_echo(payload: EchoRequest) -> dict[str, str]:
    return {"echo": payload.message}
""",
    )

    write_if_missing(
        service_root / "tests" / "test_app.py",
        """from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_secure_echo_requires_api_key() -> None:
    response = client.post("/v1/echo", json={"message": "hola"})
    assert response.status_code == 401


def test_secure_echo_with_valid_api_key() -> None:
    response = client.post(
        "/v1/echo",
        json={"message": "hola"},
        headers={"x-api-key": "dev-local-key"},
    )
    assert response.status_code == 200
""",
    )

    write_if_missing(
        service_root / "requirements.txt",
        """fastapi>=0.110.0
uvicorn>=0.29.0
pydantic>=2.7.0
""",
    )

    write_if_missing(
        service_root / "Dockerfile",
        """FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd -ms /bin/bash appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    )

    write_if_missing(
        service_root / "README.md",
        """# Python Microservice Template (FastAPI)

## Best practices included
- Health endpoint (`/healthz`) for probes.
- Input validation with Pydantic.
- Simple auth guard dependency.
- Non-root Docker runtime.
- Isolated tests for API behavior.
""",
    )
