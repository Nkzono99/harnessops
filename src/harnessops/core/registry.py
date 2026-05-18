from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

import tomli_w

from harnessops import __version__
from harnessops.core.lock import build_lock, sha256_file, write_lock
from harnessops.core.overlay import (
    default_mode,
    default_overlay_path,
    generated_overlay_files,
    overlay_dirs,
    repository_kind_for_mode,
)
from harnessops.core.project import Project
from harnessops.core.record_io import now_iso, slugify
from harnessops.profiles.registry import load_profile, profile_fingerprint


def hops_home() -> Path:
    import os

    configured = os.environ.get("HOPS_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".harnessops").resolve()


def registry_path() -> Path:
    return hops_home() / "registry.toml"


def local_project_state_root(project_id: str) -> Path:
    return hops_home() / "projects" / project_id


def read_registry() -> dict[str, Any]:
    path = registry_path()
    if not path.exists():
        return {"schema_version": "0.1", "projects": []}
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    data.setdefault("schema_version", "0.1")
    data.setdefault("projects", [])
    return data


def write_registry(data: dict[str, Any]) -> None:
    path = registry_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(tomli_w.dumps(data), encoding="utf-8", newline="\n")


def default_project_id(root: Path) -> str:
    resolved = root.resolve()
    digest = hashlib.sha1(resolved.as_posix().lower().encode("utf-8")).hexdigest()[:10]
    return f"{slugify(resolved.name)}-{digest}"


def _entry_root(entry: dict[str, Any]) -> Path:
    return Path(str(entry["root"])).expanduser().resolve()


def registry_entry_for_root(root: Path) -> dict[str, Any] | None:
    resolved = root.resolve()
    for entry in read_registry().get("projects", []) or []:
        if not isinstance(entry, dict) or "root" not in entry:
            continue
        try:
            if _entry_root(entry) == resolved:
                return entry
        except (OSError, RuntimeError):
            continue
    return None


def registry_entry_by_id(project_id: str) -> dict[str, Any] | None:
    for entry in read_registry().get("projects", []) or []:
        if isinstance(entry, dict) and entry.get("id") == project_id:
            return entry
    return None


def _project_file_for_state(state_root: Path) -> Path:
    return state_root / ".harnessops" / "project.toml"


def _write_project_file(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(tomli_w.dumps(data), encoding="utf-8", newline="\n")


def _touch_gitkeep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def _init_overlay_files(state_root: Path, overlay_mode: str, overlay_path: str, profile: dict[str, Any]) -> dict[str, str]:
    for rel in overlay_dirs(overlay_mode):
        _touch_gitkeep(state_root / overlay_path / rel)
    managed: dict[str, str] = {}
    for rel, text in generated_overlay_files(overlay_mode, overlay_path).items():
        path = state_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8", newline="\n")
        managed[rel] = sha256_file(path)
    lock = build_lock(
        harnessops_version=__version__,
        profile=profile,
        profile_fingerprint=profile_fingerprint(profile),
        overlay_mode=overlay_mode,
        overlay_path=overlay_path,
        managed_files=managed,
    )
    write_lock(state_root, lock)
    return managed


def link_local_project(
    root: Path,
    *,
    profile_id: str,
    mode: str | None = None,
    project_id: str | None = None,
    force: bool = False,
) -> Project:
    root = root.resolve()
    profile = load_profile(profile_id)
    overlay_mode = mode or default_mode(profile_id, profile)
    overlay_path = str(profile.get("feedback", {}).get("path") or default_overlay_path(overlay_mode))
    resolved_id = project_id or default_project_id(root)
    state_root = local_project_state_root(resolved_id)
    existing = registry_entry_for_root(root)
    if existing and not force:
        registered = load_registered_project(root)
        if registered is not None:
            return registered

    state_root.mkdir(parents=True, exist_ok=True)
    project_data: dict[str, Any] = {
        "schema_version": "0.1",
        "layout_version": "0.1",
        "project": {
            "name": root.name,
            "root": root.as_posix(),
            "kind": repository_kind_for_mode(overlay_mode),
        },
        "profile": {
            "id": profile_id,
            "version": str(profile.get("version", "0.1.0")),
            "source": str(profile.get("source", "builtin")),
            "adapter": str(profile.get("adapter", "generic_code")),
        },
        "overlay": {
            "mode": overlay_mode,
            "path": overlay_path,
            "storage": "local",
            "local_id": resolved_id,
            "state_root": state_root.as_posix(),
            "managed_by": "harnessops",
        },
        "privacy": {"default_visibility": "private-until-sanitized"},
        "agents": {"codex": True, "claude": False},
    }
    target_provider = profile.get("provider")
    if target_provider:
        project_data["target_harness"] = {
            "provider": target_provider,
            "manifest": ".harness/manifest.toml",
        }
    _write_project_file(_project_file_for_state(state_root), project_data)
    _init_overlay_files(state_root, overlay_mode, overlay_path, profile)

    registry = read_registry()
    entries = [
        item
        for item in registry.get("projects", []) or []
        if isinstance(item, dict)
        and item.get("id") != resolved_id
        and Path(str(item.get("root", ""))).expanduser().resolve() != root
    ]
    entries.append(
        {
            "id": resolved_id,
            "name": root.name,
            "root": root.as_posix(),
            "profile": profile_id,
            "mode": overlay_mode,
            "storage": "local",
            "state_root": state_root.as_posix(),
            "linked_at": now_iso(),
        }
    )
    registry["projects"] = entries
    write_registry(registry)
    return Project(
        root=root,
        data=project_data,
        state_root=state_root,
        project_file_path=_project_file_for_state(state_root),
        registry_id=resolved_id,
    )


def load_registered_project(root: Path) -> Project | None:
    entry = registry_entry_for_root(root)
    if entry is None:
        return None
    state_root = Path(str(entry["state_root"])).expanduser().resolve()
    project_file = _project_file_for_state(state_root)
    if not project_file.exists():
        return None
    data = tomllib.loads(project_file.read_text(encoding="utf-8"))
    return Project(
        root=root.resolve(),
        data=data,
        state_root=state_root,
        project_file_path=project_file,
        registry_id=str(entry.get("id") or ""),
    )


def unlink_local_project(root: Path, *, delete_state: bool = False) -> dict[str, Any]:
    root = root.resolve()
    registry = read_registry()
    removed: dict[str, Any] | None = None
    kept = []
    for entry in registry.get("projects", []) or []:
        if isinstance(entry, dict) and Path(str(entry.get("root", ""))).expanduser().resolve() == root:
            removed = entry
            continue
        kept.append(entry)
    registry["projects"] = kept
    write_registry(registry)
    if removed and delete_state:
        state_root = Path(str(removed["state_root"])).expanduser().resolve()
        if state_root.exists() and state_root.is_relative_to(hops_home() / "projects"):
            shutil.rmtree(state_root)
    return {"removed": removed is not None, "entry": removed}


def project_payload(project: Project) -> dict[str, Any]:
    return {
        "id": project.registry_id,
        "name": project.data.get("project", {}).get("name"),
        "root": project.root.as_posix(),
        "profile": project.profile_id,
        "mode": project.overlay_mode,
        "storage": project.overlay_storage,
        "state_root": project.storage_root.as_posix(),
        "project_file": project.project_file_path.as_posix()
        if project.project_file_path
        else None,
        "overlay_path": project.overlay_path,
        "overlay_dir": project.overlay_dir.as_posix(),
    }


def _safe_zip_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members = []
    for info in archive.infolist():
        path = Path(info.filename)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"unsafe archive member: {info.filename}")
        members.append(info)
    return members


def pack_local_project(project: Project, output: Path) -> Path:
    if project.overlay_storage != "local":
        raise ValueError("local pack には storage=local project が必要です")
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": "0.1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project": project_payload(project),
    }
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("harnessops-local-pack.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        for path in sorted(project.storage_root.rglob("*")):
            if path.is_file():
                if path.resolve() == output:
                    continue
                archive.write(path, "state/" + path.relative_to(project.storage_root).as_posix())
    return output


def import_local_pack(path: Path, *, force: bool = False) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        _safe_zip_members(archive)
        manifest = json.loads(archive.read("harnessops-local-pack.json").decode("utf-8"))
        project_info = manifest["project"]
        project_id = str(project_info["id"] or default_project_id(Path(project_info["root"])))
        state_root = local_project_state_root(project_id)
        if state_root.exists() and not force:
            raise FileExistsError(f"local state already exists: {state_root}")
        if state_root.exists():
            shutil.rmtree(state_root)
        state_root.mkdir(parents=True, exist_ok=True)
        for info in archive.infolist():
            if info.is_dir() or not info.filename.startswith("state/"):
                continue
            rel = Path(info.filename).relative_to("state")
            target = state_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(info))
    project_file = _project_file_for_state(state_root)
    data = tomllib.loads(project_file.read_text(encoding="utf-8"))
    root = Path(str(data.get("project", {}).get("root") or project_info["root"])).expanduser().resolve()
    registry = read_registry()
    entries = [
        item
        for item in registry.get("projects", []) or []
        if isinstance(item, dict) and item.get("id") != project_id
    ]
    entries.append(
        {
            "id": project_id,
            "name": str(data.get("project", {}).get("name") or root.name),
            "root": root.as_posix(),
            "profile": str(data.get("profile", {}).get("id", "")),
            "mode": str(data.get("overlay", {}).get("mode", "")),
            "storage": "local",
            "state_root": state_root.as_posix(),
            "linked_at": now_iso(),
        }
    )
    registry["projects"] = entries
    write_registry(registry)
    return {"id": project_id, "state_root": state_root, "root": root}


def merge_local_state(project: Project, source: Path) -> dict[str, Any]:
    if project.overlay_storage != "local":
        raise ValueError("local merge には storage=local project が必要です")

    def merge_from_state(source_state: Path) -> dict[str, Any]:
        source_project_file = _project_file_for_state(source_state)
        if not source_project_file.exists():
            raise FileNotFoundError(f"project.toml not found in local state: {source_state}")
        source_data = tomllib.loads(source_project_file.read_text(encoding="utf-8"))
        source_overlay = source_state / str(source_data.get("overlay", {}).get("path", project.overlay_path))
        copied: list[str] = []
        skipped: list[str] = []
        conflicted: list[str] = []
        conflict_root = project.overlay_dir / "conflicts" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        for path in sorted(source_overlay.rglob("*")):
            if not path.is_file() or "views" in path.relative_to(source_overlay).parts:
                continue
            rel = path.relative_to(source_overlay)
            target = project.overlay_dir / rel
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
                copied.append(rel.as_posix())
            elif target.read_bytes() == path.read_bytes():
                skipped.append(rel.as_posix())
            else:
                conflict = conflict_root / rel
                conflict.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, conflict)
                conflicted.append(rel.as_posix())
        return {"copied": copied, "skipped": skipped, "conflicted": conflicted}

    if source.is_dir():
        return merge_from_state(source.resolve())
    with TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(source) as archive:
            for info in _safe_zip_members(archive):
                if info.is_dir() or not info.filename.startswith("state/"):
                    continue
                rel = Path(info.filename).relative_to("state")
                target = tmp_path / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(info))
        return merge_from_state(tmp_path)
