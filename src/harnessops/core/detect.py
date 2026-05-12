from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from harnessops.adapters.harnessops_core import HarnessOpsCoreAdapter
from harnessops.adapters.paper_harness_project import PaperHarnessProjectAdapter
from harnessops.adapters.paper_harness_upstream import PaperHarnessUpstreamAdapter
from harnessops.adapters.runops_project import RunopsProjectAdapter
from harnessops.adapters.runops_upstream import RunopsUpstreamAdapter
from harnessops.core.manifest import load_manifest


def detect_repository(root: Path) -> dict[str, Any]:
    project_toml = root / ".harnessops" / "project.toml"
    if project_toml.exists():
        data = tomllib.loads(project_toml.read_text(encoding="utf-8"))
        return {
            "profile": data.get("profile", {}).get("id"),
            "repository_kind": data.get("project", {}).get("kind", "linked"),
            "source": ".harnessops/project.toml",
            "confidence": 1.0,
            "markers": [".harnessops/project.toml"],
        }

    manifest = load_manifest(root)
    recommended = manifest.get("harnessops", {}).get("recommended_profile") if manifest else None
    if recommended:
        return {
            "profile": recommended,
            "repository_kind": manifest.get("harness", {}).get("kind", "unknown"),
            "source": ".harness/manifest.toml",
            "confidence": 0.9,
            "markers": [".harness/manifest.toml"],
        }

    results = [
        RunopsProjectAdapter().detect(root),
        PaperHarnessProjectAdapter().detect(root),
        RunopsUpstreamAdapter().detect(root),
        PaperHarnessUpstreamAdapter().detect(root),
        HarnessOpsCoreAdapter().detect(root),
    ]
    best = max(results, key=lambda item: item.confidence)
    if best.profile_id:
        return {
            "profile": best.profile_id,
            "repository_kind": best.repository_kind,
            "source": "provider-markers",
            "confidence": best.confidence,
            "markers": best.markers,
        }
    if (root / "pyproject.toml").exists():
        return {
            "profile": "python-package",
            "repository_kind": "generic-repository",
            "source": "generic-markers",
            "confidence": 0.3,
            "markers": ["pyproject.toml"],
        }
    return {"profile": "generic-code", "repository_kind": "generic-repository", "source": "fallback", "confidence": 0.1, "markers": []}

