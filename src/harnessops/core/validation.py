from __future__ import annotations

from pathlib import Path
from typing import Any

from harnessops.core.lock import load_lock, sha256_file
from harnessops.core.project import Project
from harnessops.core.records import read_record
from harnessops.profiles.registry import load_profile


def validate_record(path: Path) -> list[str]:
    frontmatter, _ = read_record(path)
    errors = []
    for key in ["id", "record_type", "created_at"]:
        if key not in frontmatter:
            errors.append(f"{path}: missing {key}")
    if frontmatter.get("record_type") == "failure":
        for key in ["visibility", "disposition"]:
            if key not in frontmatter:
                errors.append(f"{path}: missing {key}")
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

