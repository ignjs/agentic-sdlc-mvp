from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from typing import Any

from orchestrator.config import CONFIG
from orchestrator.workflow import AgenticWorkflow


def run_execution_controls(root_dir: Path) -> list[dict[str, Any]]:
    """Run CI-like checks locally and return structured execution results."""
    checks = [
        ("tests", ["pytest", "-q"]),
        ("sast", ["bash", "security/scripts/run_sast.sh"]),
        ("dependency_scan", ["bash", "security/scripts/run_dependency_scan.sh"]),
    ]

    results: list[dict[str, Any]] = []
    for name, command in checks:
        completed = subprocess.run(
            command,
            cwd=str(root_dir),
            text=True,
            capture_output=True,
            check=False,
        )
        results.append(
            {
                "name": name,
                "command": " ".join(command),
                "exit_code": completed.returncode,
                "passed": completed.returncode == 0,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the agentic SDLC workflow with security guardrails")
    parser.add_argument("--intent", default=str(CONFIG.intent_path), help="Path to the project's intent file")
    parser.add_argument(
        "--project-root",
        default=str(CONFIG.root_dir),
        help="Path where the project repository/workspace should exist. If missing, a local folder is created.",
    )
    parser.add_argument(
        "--run-controls",
        action="store_true",
        help="Run local CI-like controls (pytest, SAST and dependency scan) after workflow execution.",
    )
    args = parser.parse_args()

    workflow = AgenticWorkflow(intent_path=Path(args.intent), project_root=Path(args.project_root))
    result = workflow.run()

    controls: list[dict[str, Any]] = []
    if args.run_controls:
        controls = run_execution_controls(CONFIG.root_dir)

    print(json.dumps({
        "requirements": result.requirements,
        "threat_model": result.threat_model,
        "security_report": result.security_report,
        "red_team_results": result.red_team_results,
        "patch_plan": result.patch_plan,
        "project_root": result.project_root,
        "project_root_created": result.project_root_created,
        "execution_controls": controls,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
