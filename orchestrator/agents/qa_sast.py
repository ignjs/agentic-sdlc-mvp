from __future__ import annotations

from pathlib import Path

from orchestrator.models import SecurityReport

BLOCKER_PATTERNS = [
    "eval(",
    "exec(",
    "subprocess.run(",
    "os.system(",
    "open('" ,
    "pickle.loads",
    "jwt_secret",
    "hardcoded_secret",
]


class QASASTAgent:
    """Runs a lightweight security static scan over Python sources."""

    @staticmethod
    def scan_path(path: str | Path) -> SecurityReport:
        scan_root = Path(path)
        findings: list[str] = []
        blockers: list[str] = []
        scanned_files = []

        for file_path in scan_root.rglob("*.py"):
            if ".venv" in file_path.parts:
                continue
            scanned_files.append(file_path)
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            for pattern in BLOCKER_PATTERNS:
                if pattern in content:
                    findings.append(f"Potential issue in {file_path}: {pattern}")
                    blockers.append(f"Review {file_path} for unsafe pattern: {pattern}")

        if not findings:
            summary = "Static scan passed with no obvious unsafe patterns detected."
        else:
            summary = "Static scan detected potential security issues."

        return SecurityReport(
            summary=summary,
            findings=findings,
            blockers=blockers,
            metadata={"files_scanned": len(scanned_files)},
        )
