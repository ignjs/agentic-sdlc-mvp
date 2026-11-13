from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from orchestrator.agents.code_generator import CodeGeneratorAgent
from orchestrator.agents.product_owner import ProductOwnerAgent
from orchestrator.agents.patch_agent import PatchAgent
from orchestrator.agents.qa_sast import QASASTAgent
from orchestrator.agents.red_team import RedTeamAgent
from orchestrator.agents.threat_model import ThreatModelAgent
from orchestrator.config import CONFIG
from orchestrator.sanitizer import InputSanitizer


@dataclass
class WorkflowResult:
    requirements: list[dict[str, str]]
    threat_model: list[dict[str, str]]
    security_report: dict[str, object]
    red_team_results: list[str]
    patch_plan: list[str]
    sanitized_intent: str
    project_root: str
    project_root_created: bool


class AgenticWorkflow:
    def __init__(self, intent_path: str | Path | None = None, project_root: str | Path | None = None) -> None:
        self.intent_path = Path(intent_path) if intent_path else CONFIG.intent_path
        self.project_root, self.project_root_created = self._resolve_project_root(
            Path(project_root) if project_root else CONFIG.root_dir
        )

    def run(self) -> WorkflowResult:
        sanitized_intent = InputSanitizer.sanitize_file(self.intent_path)
        requirements = ProductOwnerAgent.analyze(sanitized_intent)
        threat_model = ThreatModelAgent.analyze()
        CodeGeneratorAgent.ensure_project_layout(self.project_root, sanitized_intent)

        security_report = QASASTAgent.scan_path(self.project_root / "apps" / "template-service")
        red_team_results = RedTeamAgent.simulate(self.project_root)
        patch_plan = PatchAgent.build_patch(security_report)

        return WorkflowResult(
            requirements=[{"category": item.category, "description": item.description, "priority": item.priority} for item in requirements],
            threat_model=[{"title": item.title, "severity": item.severity, "description": item.description, "mitigation": item.mitigation} for item in threat_model],
            security_report={
                "summary": security_report.summary,
                "findings": security_report.findings,
                "blockers": security_report.blockers,
                "metadata": security_report.metadata,
            },
            red_team_results=red_team_results,
            patch_plan=patch_plan,
            sanitized_intent=sanitized_intent,
            project_root=str(self.project_root),
            project_root_created=self.project_root_created,
        )

    def _resolve_project_root(self, configured_root: Path) -> tuple[Path, bool]:
        if self._looks_like_project_repo(configured_root):
            return configured_root, False

        fallback_root = self.intent_path.parent / self._build_local_folder_name()
        fallback_root.mkdir(parents=True, exist_ok=True)
        return fallback_root, True

    @staticmethod
    def _looks_like_project_repo(path: Path) -> bool:
        if not path.exists():
            return False
        has_git = (path / ".git").exists()
        has_project_markers = (path / "pyproject.toml").is_file() or (path / "orchestrator").is_dir()
        return has_git or has_project_markers

    def _build_local_folder_name(self) -> str:
        base_name = self.intent_path.stem or "agentic-sdlc"
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", base_name).strip("-").lower()
        if not slug:
            slug = "agentic-sdlc"
        return f"{slug}-repo"
