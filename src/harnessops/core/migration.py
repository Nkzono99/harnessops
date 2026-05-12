from __future__ import annotations

from pathlib import Path
from typing import Any

from harnessops.core.lock import load_lock
from harnessops.core.project import Project


def check_migrations(project: Project) -> dict[str, Any]:
    lock = load_lock(project.root)
    pending = []
    if lock.get("layout_version") not in {None, "0.1"}:
        pending.append(f"unsupported layout_version {lock.get('layout_version')}")
    return {"pending": pending, "ok": not pending}


def apply_migrations(project: Project) -> Path | None:
    result = check_migrations(project)
    if result["pending"]:
        entry = project.root / ".harnessops" / "migrations" / "manual-migration-required.md"
        entry.parent.mkdir(parents=True, exist_ok=True)
        entry.write_text("\n".join(result["pending"]) + "\n", encoding="utf-8")
        return entry
    return None

