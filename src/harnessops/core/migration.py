from __future__ import annotations

from pathlib import Path
from typing import Any

from harnessops import __version__
from harnessops.core.lock import load_lock, write_lock
from harnessops.core.project import Project


def check_migrations(project: Project) -> dict[str, Any]:
    lock = load_lock(project.root)
    pending = []
    if lock.get("layout_version") not in {None, "0.1"}:
        pending.append(f"未対応の layout_version {lock.get('layout_version')}")
    return {"pending": pending, "ok": not pending}


def apply_migrations(project: Project) -> Path | None:
    result = check_migrations(project)
    if result["pending"]:
        lock = load_lock(project.root)
        from_version = str(lock.get("layout_version", "unknown"))
        entry = project.root / ".harnessops" / "migrations" / f"{from_version}-to-0.1.md"
        entry.parent.mkdir(parents=True, exist_ok=True)
        entry.write_text(
            "# HarnessOps レイアウトマイグレーション\n\n"
            f"- 変更元 layout_version: {from_version}\n"
            "- 変更先 layout_version: 0.1\n"
            "- アクション: 現在のMVPレイアウト向けにロックメタデータを正規化\n",
            encoding="utf-8",
        )
        lock["layout_version"] = "0.1"
        lock["schema_version"] = "0.1"
        lock["harnessops_version"] = __version__
        migrations = lock.setdefault("migrations", [])
        migrations.append(entry.name)
        write_lock(project.root, lock)
        return entry
    return None
