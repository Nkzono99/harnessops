from __future__ import annotations

from typing import Any

from harnessops.core import yamlio
from harnessops.core.lab_memory_collection import (
    build_knowledge,
    collect_abstraction_sources,
    lab_metrics,
    rel_path,
    safe_yaml,
    source_digest,
    threshold_triggers,
)
from harnessops.core.lab_memory_rendering import (
    abstraction_manifest_template,
    render_abstraction_input_markdown,
)
from harnessops.core.project import Project
from harnessops.core.record_io import now_iso


DEFAULT_MAX_FILES = 256
DEFAULT_MAX_BYTES = 2_000_000
DEFAULT_MAX_IMPROVEMENTS = 50
ABSTRACTION_MANIFEST = "knowledge/lab-memory-abstraction.yml"
ABSTRACTION_INPUT_YML = "knowledge/lab-memory-input.yml"
ABSTRACTION_INPUT_MD = "knowledge/lab-memory-input.md"
ABSTRACTION_TARGETS = [
    {
        "path": "knowledge/principles.md",
        "purpose": "採用/却下を越えて残った設計原則を source ID 付きで保つ。",
    },
    {
        "path": "knowledge/patterns.yml",
        "purpose": "再利用可能な改善パターン、適用条件、反例、ガードを構造化する。",
    },
    {
        "path": "knowledge/anti-patterns.md",
        "purpose": "繰り返し避けるべき改善劇場、過剰一般化、失敗クラスをまとめる。",
    },
    {
        "path": "knowledge/evaluation-playbook.md",
        "purpose": "評価軸、holdout、判断基準、kill criteria の経験をまとめる。",
    },
]


def _snapshot_state(project: Project, current_digest: str) -> dict[str, Any]:
    path = project.overlay_dir / "knowledge" / "lab-memory.yml"
    if not path.exists():
        return {
            "exists": False,
            "path": rel_path(project, path),
            "source_digest": None,
            "stale": True,
        }
    data = safe_yaml(path)
    sources = data.get("sources", {})
    source_digest_value = sources.get("source_digest") if isinstance(sources, dict) else None
    return {
        "exists": True,
        "path": rel_path(project, path),
        "source_digest": source_digest_value,
        "stale": source_digest_value != current_digest,
    }


def _abstraction_state(project: Project, current_digest: str) -> dict[str, Any]:
    manifest_path = project.overlay_dir / ABSTRACTION_MANIFEST
    target_states = []
    for target in ABSTRACTION_TARGETS:
        path = project.overlay_dir / target["path"]
        target_states.append(
            {
                "path": rel_path(project, path),
                "exists": path.exists(),
                "purpose": target["purpose"],
            }
        )
    if not manifest_path.exists():
        return {
            "exists": False,
            "path": rel_path(project, manifest_path),
            "source_digest": None,
            "stale": True,
            "targets": target_states,
            "missing_targets": [item["path"] for item in target_states if not item["exists"]],
        }
    data = safe_yaml(manifest_path)
    source_digest_value = data.get("source_digest")
    return {
        "exists": True,
        "path": rel_path(project, manifest_path),
        "source_digest": source_digest_value,
        "stale": source_digest_value != current_digest,
        "targets": target_states,
        "missing_targets": [item["path"] for item in target_states if not item["exists"]],
    }


def lint_lab_memory(
    project: Project,
    *,
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
    pressure = threshold_triggers(
        metrics,
        max_files=max_files,
        max_bytes=max_bytes,
        max_improvements=max_improvements,
    )
    current_digest = source_digest(project)
    snapshot = _snapshot_state(project, current_digest)
    abstraction = _abstraction_state(project, current_digest)
    has_sources = metrics["improvement_count"] > 0 or metrics["research_scan_count"] > 0
    triggers: list[str] = []
    if pressure and has_sources:
        triggers.extend(pressure)
        if not snapshot["exists"]:
            triggers.append("deterministic_snapshot_missing")
        elif snapshot["stale"]:
            triggers.append("deterministic_snapshot_stale")
        if not abstraction["exists"]:
            triggers.append("semantic_memory_missing")
        elif abstraction["stale"]:
            triggers.append("semantic_memory_stale")
        if abstraction["exists"] and abstraction["missing_targets"]:
            triggers.append("semantic_memory_targets_missing")
    status = "needs-abstraction" if triggers else "ok"
    return {
        "schema_version": "0.1",
        "kind": "harness_lab_memory_lint",
        "status": status,
        "reason": "triggers-present" if triggers else "thresholds-not-exceeded-no-sources-or-current",
        "updated_at": now_iso(),
        "metrics": metrics,
        "thresholds": thresholds,
        "source_digest": current_digest,
        "pressure": pressure,
        "triggers": triggers,
        "snapshot": snapshot,
        "abstraction": abstraction,
        "recommended_commands": [
            "hops lab memory compact --force",
            "hops lab memory prepare --force",
            "Use the hops-compact-lab-memory skill to update abstract knowledge.",
        ],
    }


def prepare_lab_memory_abstraction(
    project: Project,
    *,
    force: bool = False,
    dry_run: bool = False,
    max_files: int = DEFAULT_MAX_FILES,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_improvements: int = DEFAULT_MAX_IMPROVEMENTS,
) -> dict[str, Any]:
    lint = lint_lab_memory(
        project,
        max_files=max_files,
        max_bytes=max_bytes,
        max_improvements=max_improvements,
    )
    if not force and lint["status"] == "ok":
        return {
            "status": "skipped",
            "reason": "lint-ok",
            "lint": lint,
            "paths": [],
        }
    knowledge = build_knowledge(
        project,
        metrics=lint["metrics"],
        thresholds=lint["thresholds"],
        triggers=lint["triggers"],
        mode="abstraction-input",
    )
    data = {
        "schema_version": "0.1",
        "kind": "harness_lab_memory_abstraction_input",
        "updated_at": now_iso(),
        "lint": lint,
        "abstraction_targets": [
            {
                "path": f"{project.overlay_path}/{target['path']}",
                "purpose": target["purpose"],
            }
            for target in ABSTRACTION_TARGETS
        ],
        "deterministic_snapshot": knowledge,
        "sources": collect_abstraction_sources(project),
    }
    data["abstraction_manifest_template"] = abstraction_manifest_template(data)
    knowledge_dir = project.overlay_dir / "knowledge"
    yml_path = project.overlay_dir / ABSTRACTION_INPUT_YML
    md_path = project.overlay_dir / ABSTRACTION_INPUT_MD
    if not dry_run:
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        yml_path.write_text(yamlio.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
        md_path.write_text(render_abstraction_input_markdown(data), encoding="utf-8", newline="\n")
    return {
        "status": "dry-run" if dry_run else "written",
        "reason": "forced" if force else "lint-triggered",
        "lint": lint,
        "paths": [yml_path, md_path],
    }
