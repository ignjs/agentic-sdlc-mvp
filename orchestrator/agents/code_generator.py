from __future__ import annotations

from pathlib import Path


class CodeGeneratorAgent:
    """Generates the minimum secure codebase to satisfy the intent."""

    @staticmethod
    def build_manifest(project_root: str | Path) -> dict[str, object]:
        root = Path(project_root)
        return {
            "project_root": str(root),
            "framework": "FastAPI",
            "security_checks": [
                "input validation",
                "role authorization",
                "secret detection",
                "dependency scanning",
                "container hardening",
            ],
            "generated_files": [
                "app/main.py",
                "app/core/security.py",
                "tests/test_app.py",
                "Dockerfile",
                "requirements.txt",
            ],
        }

    @staticmethod
    def ensure_project_layout(project_root: str | Path) -> None:
        root = Path(project_root)
        (root / "apps" / "template-service" / "app").mkdir(parents=True, exist_ok=True)
        (root / "apps" / "template-service" / "tests").mkdir(parents=True, exist_ok=True)
