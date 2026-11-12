from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Requirement:
    category: str
    description: str
    priority: str = "medium"


@dataclass
class Threat:
    title: str
    severity: str
    description: str
    mitigation: str


@dataclass
class SecurityReport:
    summary: str
    findings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
