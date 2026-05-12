from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DetectionResult:
    profile_id: str | None
    repository_kind: str
    confidence: float
    markers: list[str]


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    message: str


class Adapter:
    id = "base"

    def detect(self, root: Path) -> DetectionResult:
        return DetectionResult(None, "unknown", 0.0, [])

    def default_profile_id(self, root: Path) -> str | None:
        return self.detect(root).profile_id

    def doctor_checks(self, root: Path) -> list[CheckResult]:
        return []

    def routing_hints(self, text: str) -> list[str]:
        return []

    def eval_case_templates(self) -> list[str]:
        return []

