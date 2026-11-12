from __future__ import annotations

from orchestrator.models import SecurityReport


class PatchAgent:
    """Translates security findings into actionable remediation tasks."""

    @staticmethod
    def build_patch(report: SecurityReport) -> list[str]:
        actions: list[str] = []
        if report.blockers:
            for blocker in report.blockers:
                actions.append(f"Fix root cause: {blocker}")
        if not actions:
            actions.append("No blocking issues identified; keep the code under the current safe policy.")
        return actions
