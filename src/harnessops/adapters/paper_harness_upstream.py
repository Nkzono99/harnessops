from __future__ import annotations

from pathlib import Path

from harnessops.adapters.base import Adapter, DetectionResult


class PaperHarnessUpstreamAdapter(Adapter):
    id = "paper_harness_upstream"

    def detect(self, root: Path) -> DetectionResult:
        markers = [m for m in ["template", "scripts/publish-scaffold.sh", "template/manuscript"] if (root / m).exists()]
        profile = "paper-harness-upstream" if len(markers) >= 2 else None
        return DetectionResult(profile, "target-repository", len(markers) / 3.0, markers)

