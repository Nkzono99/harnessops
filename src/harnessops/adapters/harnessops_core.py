from __future__ import annotations

from pathlib import Path

from harnessops.adapters.base import Adapter, DetectionResult


class HarnessOpsCoreAdapter(Adapter):
    id = "harnessops_core"

    def detect(self, root: Path) -> DetectionResult:
        markers = [m for m in ["pyproject.toml", "src/harnessops", "src/harnessops/profiles", "src/harnessops/schemas"] if (root / m).exists()]
        pyproject = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
        if 'name = "harnessops"' in pyproject and len(markers) >= 2:
            return DetectionResult("harnessops-core", "harnessops-repository", 0.95, markers)
        return DetectionResult(None, "unknown", 0.0, markers)

