from __future__ import annotations

from orchestrator.models import Threat


class ThreatModelAgent:
    """Creates a preliminary security threat model for the project."""

    @staticmethod
    def analyze() -> list[Threat]:
        return [
            Threat(
                title="Prompt injection against AI agents",
                severity="high",
                description="Malicious instructions hidden in repository inputs could manipulate the agent workflow.",
                mitigation="Sanitize all inputs, enforce allowlists and human review for risky prompts.",
            ),
            Threat(
                title="Broken authentication and authorization",
                severity="high",
                description="Endpoints may expose privileged actions without role verification.",
                mitigation="Enforce role checks, JWT validation and permission boundaries.",
            ),
            Threat(
                title="Injection attacks",
                severity="high",
                description="Untrusted input may be used to exploit SQL, shell or command execution flows.",
                mitigation="Validate input with Pydantic and avoid unsafe command execution.",
            ),
            Threat(
                title="Insecure file handling",
                severity="medium",
                description="Uploaded or processed files may enable path traversal or data leakage.",
                mitigation="Restrict extensions, enforce size limits and normalize paths.",
            ),
            Threat(
                title="Secret leaks and insecure configurations",
                severity="high",
                description="Environment variables or debug config may leak credentials into logs or code.",
                mitigation="Use secret managers, avoid hardcoded values and block scans for secrets.",
            ),
        ]
