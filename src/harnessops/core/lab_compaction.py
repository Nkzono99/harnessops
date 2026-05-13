from __future__ import annotations

from typing import Any

from harnessops.core import yamlio
from harnessops.core.lab_memory_collection import (
    build_knowledge,
    lab_metrics,
    threshold_triggers,
)
from harnessops.core.lab_memory_lint import (
    DEFAULT_MAX_BYTES,
    DEFAULT_MAX_FILES,
    DEFAULT_MAX_IMPROVEMENTS,
    lint_lab_memory,
    prepare_lab_memory_abstraction,
)
from harnessops.core.lab_memory_rendering import extract_curator_notes, render_markdown
from harnessops.core.project import Project

__all__ = [
    "DEFAULT_MAX_BYTES",
    "DEFAULT_MAX_FILES",
    "DEFAULT_MAX_IMPROVEMENTS",
    "compact_lab",
    "lint_lab_memory",
    "prepare_lab_memory_abstraction",
]


def compact_lab(
    project: Project,
    *,
    force: bool = False,
    dry_run: bool = False,
    max_files: int = DEFAULT_MAX_FILES,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_improvements: int = DEFAULT_MAX_IMPROVEMENTS,
) -> dict[str, Any]:
    metrics = lab_metrics(project)
    thresholds = {
        "max_files": max_files,
        "max_bytes": max_bytes,
        "max_improvements": max_improvements,
    }
    triggers = threshold_triggers(
        metrics,
        max_files=max_files,
        max_bytes=max_bytes,
        max_improvements=max_improvements,
    )
    if not force and not triggers:
        return {
            "status": "skipped",
            "reason": "thresholds-not-exceeded",
            "metrics": metrics,
            "thresholds": thresholds,
            "triggers": triggers,
            "paths": [],
        }
    mode = "forced" if force else "threshold"
    data = build_knowledge(project, metrics=metrics, thresholds=thresholds, triggers=triggers, mode=mode)
    knowledge_dir = project.overlay_dir / "knowledge"
    yml_path = knowledge_dir / "lab-memory.yml"
    md_path = knowledge_dir / "lab-memory.md"
    existing_md = md_path.read_text(encoding="utf-8") if md_path.exists() else None
    markdown = render_markdown(data, extract_curator_notes(existing_md))
    if not dry_run:
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        yml_path.write_text(yamlio.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
        md_path.write_text(markdown, encoding="utf-8", newline="\n")
    return {
        "status": "dry-run" if dry_run else "written",
        "reason": "forced" if force else "thresholds-exceeded",
        "metrics": metrics,
        "thresholds": thresholds,
        "triggers": triggers,
        "paths": [yml_path, md_path],
    }
