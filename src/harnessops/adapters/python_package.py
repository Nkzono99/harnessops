from __future__ import annotations

from pathlib import Path

from harnessops.adapters.base import Adapter, DetectionResult


class PythonPackageAdapter(Adapter):
    id = "python_package"

    def detect(self, root: Path) -> DetectionResult:
        markers = ["pyproject.toml"] if (root / "pyproject.toml").exists() else []
        return DetectionResult("python-package" if markers else None, "python-package", 0.4, markers)

