from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

PACKAGED_SKILL_HOSTS = ("codex", "claude")


def _assert_within(root: Path, path: Path) -> None:
    root_resolved = root.resolve()
    path_resolved = path.resolve()
    if root_resolved != path_resolved and root_resolved not in path_resolved.parents:
        raise ValueError(f"path escapes expected root: {path}")


def _repo_skill_files(root: Path) -> dict[Path, bytes]:
    skills_root = root / ".agents" / "skills"
    if not skills_root.exists():
        raise FileNotFoundError(f"repo-local skills directory not found: {skills_root}")
    files: dict[Path, bytes] = {}
    for skill_dir in sorted(path for path in skills_root.glob("hops-*") if path.is_dir()):
        if not (skill_dir / "SKILL.md").exists():
            continue
        for source_file in sorted(path for path in skill_dir.rglob("*") if path.is_file()):
            files[source_file.relative_to(skills_root)] = source_file.read_bytes()
    return files


def sync_packaged_skill_assets(
    root: Path,
    *,
    hosts: tuple[str, ...] = PACKAGED_SKILL_HOSTS,
    check: bool = False,
) -> dict[str, Any]:
    """Sync repo-local hops skills into packaged codex/claude asset directories."""
    invalid_hosts = sorted(set(hosts) - set(PACKAGED_SKILL_HOSTS))
    if invalid_hosts:
        raise ValueError("unknown packaged skill host: " + ", ".join(invalid_hosts))

    root = root.resolve()
    source_files = _repo_skill_files(root)
    if not source_files:
        raise FileNotFoundError("no repo-local hops skills found under .agents/skills")

    asset_root = root / "src" / "harnessops" / "agent_assets" / "skills"
    result: dict[str, Any] = {
        "ok": True,
        "check": check,
        "hosts": list(hosts),
        "checked": [],
        "updated": [],
        "unchanged": [],
        "missing": [],
        "drifted": [],
        "retired": [],
    }

    for host in hosts:
        host_skills_root = asset_root / host / "harnessops" / "skills"
        _assert_within(asset_root, host_skills_root)
        if not host_skills_root.exists() and check:
            result["missing"].append(host_skills_root.relative_to(root).as_posix())
            continue
        if not check:
            host_skills_root.mkdir(parents=True, exist_ok=True)

        desired_rels = set(source_files)
        for rel, source_bytes in source_files.items():
            target = host_skills_root / rel
            _assert_within(host_skills_root, target)
            rel_path = target.relative_to(root).as_posix()
            result["checked"].append(rel_path)
            if not target.exists():
                result["missing"].append(rel_path)
                if not check:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(source_bytes)
                    result["updated"].append(rel_path)
                continue
            if target.read_bytes() == source_bytes:
                result["unchanged"].append(rel_path)
                continue
            result["drifted"].append(rel_path)
            if not check:
                target.write_bytes(source_bytes)
                result["updated"].append(rel_path)

        if host_skills_root.exists():
            for skill_dir in sorted(path for path in host_skills_root.glob("hops-*") if path.is_dir()):
                if skill_dir.name in {rel.parts[0] for rel in desired_rels}:
                    continue
                _assert_within(host_skills_root, skill_dir)
                rel_path = skill_dir.relative_to(root).as_posix()
                result["retired"].append(rel_path)
                if not check:
                    shutil.rmtree(skill_dir)

    if check and (result["missing"] or result["drifted"] or result["retired"]):
        result["ok"] = False
    return result
