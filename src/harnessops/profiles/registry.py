from __future__ import annotations

import hashlib
import importlib.resources
from pathlib import Path
from typing import Any

import yaml

BUILTIN_PACKAGE = "harnessops.profiles.builtins"


def _read_builtin_text(name: str) -> str:
    return importlib.resources.files(BUILTIN_PACKAGE).joinpath(name).read_text(encoding="utf-8")


def builtin_profile_names() -> list[str]:
    files = importlib.resources.files(BUILTIN_PACKAGE).iterdir()
    return sorted(path.name for path in files if path.name.endswith((".yml", ".yaml")))


def load_builtin_profiles() -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    for name in builtin_profile_names():
        text = _read_builtin_text(name)
        data = yaml.safe_load(text) or {}
        data.setdefault("source", "builtin")
        data["_raw"] = text
        profiles[data["id"]] = data
    return profiles


def load_profile(profile_id_or_path: str) -> dict[str, Any]:
    candidate = Path(profile_id_or_path)
    if candidate.exists():
        text = candidate.read_text(encoding="utf-8")
        data = yaml.safe_load(text) or {}
        data.setdefault("source", "local")
        data["_raw"] = text
        return data
    profiles = load_builtin_profiles()
    if profile_id_or_path not in profiles:
        raise KeyError(f"profile not found: {profile_id_or_path}")
    return profiles[profile_id_or_path]


def profile_fingerprint(profile: dict[str, Any]) -> str:
    raw = str(profile.get("_raw") or yaml.safe_dump(profile, sort_keys=True))
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def profile_ids() -> list[str]:
    return sorted(load_builtin_profiles())

