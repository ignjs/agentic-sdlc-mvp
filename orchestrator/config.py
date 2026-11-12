from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AppConfig:
    root_dir: Path = ROOT_DIR
    intent_path: Path = ROOT_DIR / "intent.md"
    app_dir: Path = ROOT_DIR / "apps" / "template-service"
    security_dir: Path = ROOT_DIR / "security"
    logs_dir: Path = ROOT_DIR / "logs"


CONFIG = AppConfig()
