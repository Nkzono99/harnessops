from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def lock_path(root: Path) -> Path:
    return root / ".harnessops" / "lock.json"


def load_lock(root: Path) -> dict[str, Any]:
    path = lock_path(root)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_lock(root: Path, lock: dict[str, Any]) -> None:
    path = lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_lock(
    *,
    harnessops_version: str,
    profile: dict[str, Any],
    profile_fingerprint: str,
    overlay_mode: str,
    overlay_path: str,
    managed_files: dict[str, str],
) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "layout_version": "0.1",
        "harnessops_version": harnessops_version,
        "profile": {
            "id": profile["id"],
            "version": str(profile.get("version", "0.1.0")),
            "source": str(profile.get("source", "builtin")),
            "fingerprint": profile_fingerprint,
        },
        "overlay": {"mode": overlay_mode, "path": overlay_path},
        "managed_files": managed_files,
        "migrations": [],
    }

