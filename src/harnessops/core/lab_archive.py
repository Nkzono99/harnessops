from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from harnessops.core.project import Project

ARCHIVE_POLICY_VERSION = 1


def _posix(path: Path | str) -> str:
    return Path(path).as_posix()


def _run_git(
    root: Path, args: list[str], *, text: bool = True
) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=text,
    )
    if result.returncode != 0:
        stderr = (
            result.stderr.strip()
            if isinstance(result.stderr, str)
            else result.stderr.decode("utf-8", "replace")
        )
        stdout = (
            result.stdout.strip()
            if isinstance(result.stdout, str)
            else result.stdout.decode("utf-8", "replace")
        )
        detail = stderr or stdout or f"git {' '.join(args)} failed"
        raise RuntimeError(detail)
    return result


def _rev_parse(root: Path, ref: str) -> str:
    result = _run_git(root, ["rev-parse", "--verify", f"{ref}^{{commit}}"])
    return str(result.stdout).strip()


def _first_parent(root: Path, commit: str) -> str | None:
    result = _run_git(root, ["rev-list", "--parents", "-n", "1", commit])
    parts = str(result.stdout).strip().split()
    if len(parts) < 2:
        return None
    return parts[1]


def _slug_ref(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return slug.strip("-") or "ref"


def _archive_prefixes(project: Project) -> tuple[str, ...]:
    overlay = project.overlay_path.strip("/\\")
    return (
        f"{overlay}/records/",
        f"{overlay}/improvements/",
    )


def _is_archivable(path: str, project: Project) -> bool:
    normalized = Path(path).as_posix()
    return any(normalized.startswith(prefix) for prefix in _archive_prefixes(project))


def _deleted_paths_in_commit(project: Project, commit: str) -> list[str]:
    overlay = project.overlay_path.strip("/\\")
    result = _run_git(
        project.root,
        [
            "diff-tree",
            "--no-commit-id",
            "--name-status",
            "-r",
            "--diff-filter=D",
            commit,
            "--",
            overlay,
        ],
    )
    paths: list[str] = []
    for line in str(result.stdout).splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0] == "D":
            paths.append(Path(parts[1]).as_posix())
    return paths


def _deleted_commits(project: Project, since_ref: str, to_ref: str) -> list[str]:
    overlay = project.overlay_path.strip("/\\")
    result = _run_git(
        project.root,
        [
            "log",
            "--format=%H",
            "--diff-filter=D",
            f"{since_ref}..{to_ref}",
            "--",
            overlay,
        ],
    )
    return [line.strip() for line in str(result.stdout).splitlines() if line.strip()]


def _git_show_bytes(root: Path, ref: str, path: str) -> bytes:
    result = _run_git(root, ["show", f"{ref}:{path}"], text=False)
    return bytes(result.stdout)


def plan_lab_archive(
    project: Project, *, since_ref: str, to_ref: str = "HEAD"
) -> dict[str, Any]:
    """Plan a release archive pack for deleted harness-lab source records."""

    since_commit = _rev_parse(project.root, since_ref)
    to_commit = _rev_parse(project.root, to_ref)
    entries: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    seen_events: set[tuple[str, str]] = set()

    for delete_commit in _deleted_commits(project, since_ref, to_ref):
        parent = _first_parent(project.root, delete_commit)
        if parent is None:
            continue
        for original_path in _deleted_paths_in_commit(project, delete_commit):
            event_key = (delete_commit, original_path)
            if event_key in seen_events:
                continue
            seen_events.add(event_key)
            if not _is_archivable(original_path, project):
                excluded.append(
                    {
                        "path": original_path,
                        "delete_commit": delete_commit,
                        "reason": "outside-archive-policy",
                    }
                )
                continue
            try:
                content = _git_show_bytes(project.root, parent, original_path)
            except RuntimeError as exc:
                excluded.append(
                    {
                        "path": original_path,
                        "delete_commit": delete_commit,
                        "reason": f"content-unavailable: {exc}",
                    }
                )
                continue
            digest = hashlib.sha256(content).hexdigest()
            archive_path = f"deleted/{delete_commit[:12]}/{original_path}"
            entries.append(
                {
                    "path": original_path,
                    "archive_path": archive_path,
                    "delete_commit": delete_commit,
                    "source_ref": parent,
                    "sha256": digest,
                    "size_bytes": len(content),
                }
            )

    entries.sort(key=lambda item: (str(item["path"]), str(item["delete_commit"])))
    return {
        "ok": True,
        "kind": "harness_lab_archive_plan",
        "policy_version": ARCHIVE_POLICY_VERSION,
        "since_ref": since_ref,
        "to_ref": to_ref,
        "since_commit": since_commit,
        "to_commit": to_commit,
        "overlay_path": project.overlay_path,
        "include_prefixes": list(_archive_prefixes(project)),
        "deleted_count": len(entries) + len(excluded),
        "eligible_count": len(entries),
        "entries": entries,
        "excluded": excluded,
    }


def _manifest_for_plan(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "harness_lab_archive_pack",
        "policy_version": ARCHIVE_POLICY_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": {
            "since_ref": plan["since_ref"],
            "to_ref": plan["to_ref"],
            "since_commit": plan["since_commit"],
            "to_commit": plan["to_commit"],
        },
        "overlay_path": plan["overlay_path"],
        "include_prefixes": plan["include_prefixes"],
        "entries": plan["entries"],
        "excluded": plan["excluded"],
    }


def pack_lab_archive(
    project: Project,
    *,
    since_ref: str,
    to_ref: str = "HEAD",
    out_dir: Path,
    asset_name: str | None = None,
) -> dict[str, Any]:
    plan = plan_lab_archive(project, since_ref=since_ref, to_ref=to_ref)
    if plan["eligible_count"] == 0:
        return {
            "ok": True,
            "status": "empty",
            "path": None,
            "archive_sha256": None,
            "plan": plan,
        }

    out_dir.mkdir(parents=True, exist_ok=True)
    archive_name = (
        asset_name
        or f"harness-lab-archive-{_slug_ref(since_ref)}-to-{_slug_ref(to_ref)}.zip"
    )
    archive_path = out_dir / archive_name
    manifest = _manifest_for_plan(plan)
    manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")

    sums: list[tuple[str, str]] = []
    with zipfile.ZipFile(
        archive_path, "w", compression=zipfile.ZIP_DEFLATED
    ) as archive:
        for entry in plan["entries"]:
            content = _git_show_bytes(
                project.root, str(entry["source_ref"]), str(entry["path"])
            )
            archive.writestr(str(entry["archive_path"]), content)
            sums.append(
                (hashlib.sha256(content).hexdigest(), str(entry["archive_path"]))
            )
        archive.writestr("manifest.json", manifest_bytes)
        sums.append((hashlib.sha256(manifest_bytes).hexdigest(), "manifest.json"))
        sums_text = "".join(
            f"{digest}  {path}\n"
            for digest, path in sorted(sums, key=lambda item: item[1])
        )
        archive.writestr("SHA256SUMS", sums_text.encode("utf-8"))

    archive_digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    return {
        "ok": True,
        "status": "written",
        "path": archive_path,
        "archive_sha256": archive_digest,
        "manifest": manifest,
        "plan": plan,
    }


def verify_lab_archive(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    if not path.exists():
        return {
            "ok": False,
            "status": "missing",
            "path": path,
            "errors": [f"archive not found: {_posix(path)}"],
        }

    try:
        with zipfile.ZipFile(path, "r") as archive:
            names = set(archive.namelist())
            if "manifest.json" not in names:
                errors.append("missing manifest.json")
                manifest: dict[str, Any] = {}
            else:
                manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
            if "SHA256SUMS" not in names:
                errors.append("missing SHA256SUMS")
                sums: dict[str, str] = {}
            else:
                sums = {}
                for line in archive.read("SHA256SUMS").decode("utf-8").splitlines():
                    if not line.strip():
                        continue
                    digest, _, member_path = line.partition("  ")
                    if not digest or not member_path:
                        errors.append(f"invalid SHA256SUMS line: {line}")
                        continue
                    sums[member_path] = digest

            for member_path, expected_digest in sums.items():
                if member_path not in names:
                    errors.append(f"missing member listed in SHA256SUMS: {member_path}")
                    continue
                actual_digest = hashlib.sha256(archive.read(member_path)).hexdigest()
                if actual_digest != expected_digest:
                    errors.append(f"sha256 mismatch: {member_path}")

            for entry in manifest.get("entries", []):
                archive_path = str(entry.get("archive_path", ""))
                if archive_path not in sums:
                    errors.append(
                        f"manifest entry missing from SHA256SUMS: {archive_path}"
                    )
                if archive_path in names and entry.get("sha256"):
                    actual_digest = hashlib.sha256(
                        archive.read(archive_path)
                    ).hexdigest()
                    if actual_digest != entry["sha256"]:
                        errors.append(f"manifest sha256 mismatch: {archive_path}")
    except (OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        return {"ok": False, "status": "invalid", "path": path, "errors": [str(exc)]}

    archive_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "ok": not errors,
        "status": "ok" if not errors else "invalid",
        "path": path,
        "archive_sha256": archive_digest,
        "entry_count": len(manifest.get("entries", []))
        if "manifest" in locals()
        else 0,
        "source": manifest.get("source", {}) if "manifest" in locals() else {},
        "errors": errors,
    }
