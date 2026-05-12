from __future__ import annotations

from pathlib import Path
from typing import Any

from harnessops.core.lock import load_lock, sha256_file
from harnessops.core.project import Project
from harnessops.core.records import read_record
from harnessops.core.routing import DISPOSITIONS
from harnessops.profiles.registry import load_profile

ID_PREFIX_BY_TYPE = {
    "failure": "F",
    "local_workaround": "LW",
    "upstream_feedback": "UF",
    "meta_feedback": "MF",
    "imported_feedback": "FB",
    "eval_case": "E",
    "hypothesis": "H",
    "experiment": "X",
    "decision": "D",
}

REQUIRED_SECTIONS = {
    "failure": ["Context", "What happened", "Why this matters", "Desired behavior", "Local workaround", "Routing rationale"],
    "upstream_feedback": ["Summary", "Minimal reproduction", "Expected upstream improvement", "Private info excluded"],
    "meta_feedback": ["Summary", "Minimal reproduction", "Expected upstream improvement", "Private info excluded"],
    "imported_feedback": ["Summary", "Reproduction", "Expected upstream change"],
    "eval_case": ["Fixture", "Task", "Expected behavior", "Pass criteria", "Fail criteria"],
    "hypothesis": [
        "Hypothesis",
        "Mechanism",
        "Minimal implementation",
        "Alternative: deletion or consolidation",
        "Expected upside",
        "Expected downside",
        "Evaluation plan",
        "Kill criteria",
    ],
    "decision": ["Decision", "Reason", "Evidence", "Regression risk", "Follow-up", "Regression guard"],
}


def validate_record(path: Path) -> list[str]:
    frontmatter, body = read_record(path)
    errors = []
    for key in ["id", "record_type", "created_at"]:
        if key not in frontmatter:
            errors.append(f"{path}: missing {key}")
    record_type = frontmatter.get("record_type")
    record_id = str(frontmatter.get("id", ""))
    expected_prefix = ID_PREFIX_BY_TYPE.get(str(record_type))
    if expected_prefix and not record_id.startswith(expected_prefix):
        errors.append(f"{path}: id prefix does not match record_type")
    if record_type == "failure":
        for key in ["visibility", "disposition"]:
            if key not in frontmatter:
                errors.append(f"{path}: missing {key}")
        disposition = frontmatter.get("disposition", {})
        if disposition.get("type") not in DISPOSITIONS:
            errors.append(f"{path}: invalid disposition")
    if record_type in {"upstream_feedback", "meta_feedback"} and "sanitized" not in frontmatter:
        errors.append(f"{path}: feedback record missing sanitized flag")
    if record_type == "imported_feedback":
        for key in ["source", "classification", "links"]:
            if key not in frontmatter:
                errors.append(f"{path}: imported feedback missing {key}")
    if record_type == "eval_case":
        for key in ["capability", "failure_class", "source_feedback"]:
            if key not in frontmatter:
                errors.append(f"{path}: eval case missing {key}")
    if record_type == "hypothesis":
        for key in ["target_capability", "source_eval_case"]:
            if key not in frontmatter:
                errors.append(f"{path}: hypothesis missing {key}")
    if record_type == "decision":
        if "source" not in frontmatter:
            errors.append(f"{path}: decision missing source")
        if frontmatter.get("status") == "adopted":
            evidence = frontmatter.get("evidence", {})
            if not evidence.get("summary") or not evidence.get("guard_path"):
                errors.append(f"{path}: adopted decision requires evidence summary and guard_path")
    for section in REQUIRED_SECTIONS.get(str(record_type), []):
        if f"## {section}" not in body:
            errors.append(f"{path}: missing section {section}")
    if "TODO" in body:
        errors.append(f"{path}: unresolved TODO placeholder")
    return errors


def doctor(project: Project, *, check_records: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        load_profile(project.profile_id)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"profile not found: {exc}")
    if not project.overlay_dir.exists():
        errors.append(f"overlay missing: {project.overlay_path}")
    required_dirs = (
        ["records/failures", "records/local-workarounds", "records/upstream-feedback", "records/meta-feedback", "views"]
        if project.overlay_mode in {"feedback-source", "local-and-feedback"}
        else ["records/feedback", "records/eval-cases", "records/hypotheses", "records/experiments", "records/decisions", "views"]
    )
    for rel in required_dirs:
        if not (project.overlay_dir / rel).exists():
            errors.append(f"missing overlay directory: {project.overlay_path}/{rel}")
    lock = load_lock(project.root)
    if not lock:
        errors.append(".harnessops/lock.json missing")
    if lock and lock.get("overlay", {}).get("path") != project.overlay_path:
        errors.append("lock overlay path does not match project.toml")
    managed = lock.get("managed_files", {}) if isinstance(lock.get("managed_files"), dict) else {}
    for rel, expected_hash in managed.items():
        path = project.root / rel
        if not path.exists():
            errors.append(f"managed file missing: {rel}")
        elif sha256_file(path) != expected_hash:
            warnings.append(f"generated view stale or edited: {rel}")
    if check_records and project.overlay_dir.exists():
        for path in project.overlay_dir.glob("records/**/*.md"):
            errors.extend(validate_record(path))
    return {"ok": not errors, "errors": errors, "warnings": warnings}
