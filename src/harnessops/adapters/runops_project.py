from __future__ import annotations

from pathlib import Path

from harnessops.adapters.base import Adapter, CheckResult, DetectionResult


class RunopsProjectAdapter(Adapter):
    id = "runops_project"

    def detect(self, root: Path) -> DetectionResult:
        markers = [m for m in [".runops/harness.lock", "campaign.toml", "cases", "runs"] if (root / m).exists()]
        profile = "runops-project" if len(markers) >= 2 else None
        return DetectionResult(profile, "project-repository", len(markers) / 4.0, markers)

    def doctor_checks(self, root: Path) -> list[CheckResult]:
        checks = []
        for marker in ["campaign.toml", "cases", "runs"]:
            checks.append(CheckResult(marker, (root / marker).exists(), f"{marker} exists"))
        return checks

