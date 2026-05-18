from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any

from harnessops.core.lock import sha256_file
from harnessops.core.managed_files import conflict_path


def packaged_global_plugin_source(host: str = "codex") -> Path:
    return Path(
        str(
            resources.files("harnessops").joinpath(
                "agent_assets", "plugins", host, "harnessops-global"
            )
        )
    )


def default_user_plugin_dir(host: str = "codex") -> Path:
    if host != "codex":
        raise ValueError(f"unsupported global plugin host: {host}")
    return Path.home() / ".codex" / "plugins" / "harnessops-global"


def install_global_plugin(
    *,
    host: str = "codex",
    destination: Path | None = None,
    force: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    source = packaged_global_plugin_source(host)
    if not source.exists():
        raise FileNotFoundError(f"global plugin asset not found: {source}")
    destination = (destination or default_user_plugin_dir(host)).expanduser().resolve()
    checked: list[str] = []
    updated: list[str] = []
    unchanged: list[str] = []
    written_new: list[dict[str, str]] = []
    for source_file in sorted(path for path in source.rglob("*") if path.is_file()):
        rel = source_file.relative_to(source).as_posix()
        target = destination / rel
        checked.append(rel)
        text = source_file.read_text(encoding="utf-8")
        if not target.exists():
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8", newline="\n")
            updated.append(rel)
            continue
        if target.read_text(encoding="utf-8") == text:
            unchanged.append(rel)
            continue
        if force:
            if not dry_run:
                target.write_text(text, encoding="utf-8", newline="\n")
            updated.append(rel)
            continue
        conflict = conflict_path(target, text)
        if not dry_run:
            conflict.write_text(text, encoding="utf-8", newline="\n")
        written_new.append({"path": rel, "new": conflict.as_posix()})
    manifest = destination / ".codex-plugin" / "plugin.json"
    return {
        "host": host,
        "destination": destination.as_posix(),
        "manifest": manifest.as_posix(),
        "checked": checked,
        "updated": updated,
        "unchanged": unchanged,
        "written_new": written_new,
        "fingerprint": sha256_file(manifest) if manifest.exists() else None,
    }
