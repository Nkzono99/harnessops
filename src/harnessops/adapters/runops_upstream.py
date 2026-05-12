from __future__ import annotations

from pathlib import Path

from harnessops.adapters.base import Adapter, DetectionResult


class RunopsUpstreamAdapter(Adapter):
    id = "runops_upstream"

    def detect(self, root: Path) -> DetectionResult:
        markers = [m for m in ["pyproject.toml", "src/runops", "src/runops/templates"] if (root / m).exists()]
        pyproject = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
        if 'name = "runops"' in pyproject and len(markers) >= 2:
            return DetectionResult("runops-upstream", "target-repository", 0.95, markers)
        return DetectionResult(None, "unknown", 0.0, markers)

