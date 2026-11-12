from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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


class AgenticWorkflow:
    def __init__(self, intent_path: str | Path | None = None) -> None:
        self.intent_path = Path(intent_path) if intent_path else CONFIG.intent_path
        self.project_root = CONFIG.root_dir

    def run(self) -> WorkflowResult:
        sanitized_intent = InputSanitizer.sanitize_file(self.intent_path)
        requirements = ProductOwnerAgent.analyze(sanitized_intent)
        threat_model = ThreatModelAgent.analyze()
        CodeGeneratorAgent.ensure_project_layout(self.project_root)

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
        )
