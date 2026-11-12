from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrator.config import CONFIG
from orchestrator.workflow import AgenticWorkflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the agentic SDLC workflow with security guardrails")
    parser.add_argument("--intent", default=str(CONFIG.intent_path), help="Path to the project's intent file")
    args = parser.parse_args()

    workflow = AgenticWorkflow(intent_path=Path(args.intent))
    result = workflow.run()

    print(json.dumps({
        "requirements": result.requirements,
        "threat_model": result.threat_model,
        "security_report": result.security_report,
        "red_team_results": result.red_team_results,
        "patch_plan": result.patch_plan,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
