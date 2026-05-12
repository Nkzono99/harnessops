from __future__ import annotations

from pathlib import Path

from harnessops.adapters.base import Adapter, CheckResult, DetectionResult


class PaperHarnessProjectAdapter(Adapter):
    id = "paper_harness_project"

    def detect(self, root: Path) -> DetectionResult:
        markers = [m for m in ["manuscript", "notes/claim-evidence-map.md", "refs", "submission"] if (root / m).exists()]
        profile = "paper-harness-project" if len(markers) >= 2 else None
        return DetectionResult(profile, "project-repository", len(markers) / 4.0, markers)

    def doctor_checks(self, root: Path) -> list[CheckResult]:
        return [
            CheckResult("manuscript", (root / "manuscript").exists(), "manuscript exists"),
            CheckResult("notes", (root / "notes").exists(), "notes exists"),
        ]

