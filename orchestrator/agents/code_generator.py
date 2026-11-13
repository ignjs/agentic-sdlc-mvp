from __future__ import annotations

from pathlib import Path

from orchestrator.agents.generators import (
    scaffold_angular_frontend,
    scaffold_go_microservice,
    scaffold_liquid_landing,
    scaffold_python_microservice,
    scaffold_react_frontend,
    scaffold_spring_boot_microservice,
)
from orchestrator.agents.generators.common import has_all_keywords, has_any_keyword


class CodeGeneratorAgent:
    """Coordinates stack-specific scaffolders based on the intent."""

    @staticmethod
    def build_manifest(project_root: str | Path) -> dict[str, object]:
        root = Path(project_root)
        return {
            "project_root": str(root),
            "frameworks": ["FastAPI", "Spring Boot", "Go net/http", "React", "Angular"],
            "security_checks": [
                "input validation",
                "role authorization",
                "secret detection",
                "dependency scanning",
                "container hardening",
            ],
            "generated_files": [
                "apps/template-service/*",
                "apps/springboot-microservice/*",
                "apps/go-microservice/*",
                "apps/liquid-landing/*",
                "apps/react-frontend/*",
                "apps/angular-frontend/*",
            ],
        }

    @staticmethod
    def ensure_project_layout(project_root: str | Path, intent_text: str = "") -> None:
        root = Path(project_root)
        normalized_intent = intent_text.lower()

        if CodeGeneratorAgent._wants_python_microservice(normalized_intent):
            scaffold_python_microservice(root)

        if CodeGeneratorAgent._wants_liquid_html(normalized_intent):
            scaffold_liquid_landing(root)
        if CodeGeneratorAgent._wants_go_microservice(normalized_intent):
            scaffold_go_microservice(root)
        if CodeGeneratorAgent._wants_spring_boot_microservice(normalized_intent):
            scaffold_spring_boot_microservice(root)
        if CodeGeneratorAgent._wants_react_frontend(normalized_intent):
            scaffold_react_frontend(root)
        if CodeGeneratorAgent._wants_angular_frontend(normalized_intent):
            scaffold_angular_frontend(root)

    @staticmethod
    def _wants_liquid_html(intent_text: str) -> bool:
        return has_all_keywords(intent_text, ("html", "liquid")) and has_any_keyword(
            intent_text,
            ("portada", "landing", "cover"),
        )

    @staticmethod
    def _wants_go_microservice(intent_text: str) -> bool:
        return has_any_keyword(intent_text, ("go", "golang")) and has_any_keyword(
            intent_text,
            ("microservicio", "microservice", "api"),
        )

    @staticmethod
    def _wants_python_microservice(intent_text: str) -> bool:
        stack_signal = has_any_keyword(intent_text, ("python", "fastapi"))
        service_signal = has_any_keyword(intent_text, ("microservicio", "microservice", "api", "backend"))
        return stack_signal or service_signal

    @staticmethod
    def _wants_spring_boot_microservice(intent_text: str) -> bool:
        return has_any_keyword(intent_text, ("spring", "springboot", "spring boot")) and has_any_keyword(
            intent_text,
            ("microservicio", "microservice", "api"),
        )

    @staticmethod
    def _wants_react_frontend(intent_text: str) -> bool:
        return has_any_keyword(intent_text, ("react",)) and has_any_keyword(
            intent_text,
            ("frontend", "front-end", "web", "ui", "landing"),
        )

    @staticmethod
    def _wants_angular_frontend(intent_text: str) -> bool:
        return has_any_keyword(intent_text, ("angular",)) and has_any_keyword(
            intent_text,
            ("frontend", "front-end", "web", "ui", "landing"),
        )
