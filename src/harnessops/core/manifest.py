from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

import tomli_w


def manifest_path(root: Path) -> Path:
    return root / ".harness" / "manifest.toml"


def load_manifest(root: Path) -> dict[str, Any]:
    path = manifest_path(root)
    if not path.exists():
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def default_manifest(profile: dict[str, Any]) -> dict[str, Any]:
    profile_id = profile["id"]
    provider = str(profile.get("provider") or profile_id.replace("-project", "").replace("-upstream", ""))
    kind = str(profile.get("repository_kind", "generated-project"))
    commands = {"doctor": "hops doctor", "migrate": "hops migrate", "version": "hops version"}
    if provider == "runops":
        commands = {
            "doctor": "runo doctor",
            "update": "runo update-harness",
            "migrate": "runo migrate",
            "feedback": "runo feedback",
            "version": "runo version",
        }
    elif provider == "paper-harness":
        executable = "pops" if profile_id == "paper-harness-upstream" else "paper-harness"
        commands = {
            "doctor": f"{executable} doctor",
            "update": f"{executable} update-harness",
            "migrate": f"{executable} migrate",
            "feedback": f"{executable} feedback",
            "version": f"{executable} version",
        }
    return {
        "schema_version": "0.1",
        "harness": {"provider": provider, "kind": kind, "version": "0.1.0"},
        "commands": commands,
        "harnessops": {"recommended_profile": profile_id},
    }


def write_manifest(root: Path, profile: dict[str, Any], *, force: bool = False) -> None:
    path = manifest_path(root)
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(tomli_w.dumps(default_manifest(profile)), encoding="utf-8")
