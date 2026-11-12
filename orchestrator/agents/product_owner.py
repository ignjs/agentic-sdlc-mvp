from __future__ import annotations

from pathlib import Path

from orchestrator.models import Requirement


class ProductOwnerAgent:
    """Extracts requirements from intent.md and prioritizes the implementation."""

    @staticmethod
    def analyze(intent_text: str) -> list[Requirement]:
        text = intent_text.lower()
        requirements: list[Requirement] = []

        mapping = {
            "usuarios": "user_management",
            "autenticación": "authentication",
            "documentos": "document_management",
            "roles": "role_based_access",
            "auditoría": "audit_logging",
            "api": "rest_api",
            "docker": "dockerization",
            "seguridad": "security_controls",
        }

        for keyword, category in mapping.items():
            if keyword in text:
                requirements.append(
                    Requirement(
                        category=category,
                        description=f"Support {keyword} capability in the delivery pipeline.",
                        priority="high" if keyword in {"autenticación", "seguridad", "api"} else "medium",
                    )
                )

        if not requirements:
            requirements.append(
                Requirement(
                    category="baseline",
                    description="Define the minimum viable specification to proceed.",
                    priority="high",
                )
            )

        return requirements

    @staticmethod
    def from_file(intent_path: str | Path) -> list[Requirement]:
        path = Path(intent_path)
        return ProductOwnerAgent.analyze(path.read_text(encoding="utf-8"))
