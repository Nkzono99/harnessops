from __future__ import annotations

import datetime as dt
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import typer

from harnessops import __version__
from harnessops.core.lock import load_lock
from harnessops.core.paths import find_root

NOTICE_INTERVAL = dt.timedelta(days=7)
NOTICE_CACHE = "update-notice.json"
DISABLE_ENV_VARS = ("HOPS_DISABLE_UPDATE_NOTICE", "HARNESSOPS_DISABLE_UPDATE_NOTICE")
SKIPPED_COMMANDS = {"update-harness", "version"}


@dataclass(frozen=True)
class UpdateNotice:
    recorded_version: str
    current_version: str


def _truthy(value: str | None) -> bool:
    return value is not None and value.strip().lower() in {"1", "true", "yes", "on"}


def _version_parts(value: str) -> tuple[int, ...]:
    parts = [int(part) for part in re.findall(r"\d+", value)]
    return tuple(parts) if parts else (0,)


def _is_older(recorded: str, current: str) -> bool:
    recorded_parts = _version_parts(recorded)
    current_parts = _version_parts(current)
    length = max(len(recorded_parts), len(current_parts))
    recorded_parts = recorded_parts + (0,) * (length - len(recorded_parts))
    current_parts = current_parts + (0,) * (length - len(current_parts))
    return recorded_parts < current_parts


def _cache_path(root: Path) -> Path:
    return root / ".harnessops" / "cache" / NOTICE_CACHE


def _parse_time(value: object) -> dt.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def _load_notice_cache(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}


def _write_notice_cache(path: Path, notice: UpdateNotice, now: dt.datetime) -> None:
    payload = {
        "schema_version": "0.1",
        "kind": "harnessops_update_notice",
        "last_notice_at": now.isoformat(),
        "recorded_harnessops_version": notice.recorded_version,
        "current_harnessops_version": notice.current_version,
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError:
        return


def _recently_notified(path: Path, notice: UpdateNotice, now: dt.datetime) -> bool:
    cache = _load_notice_cache(path)
    if cache.get("recorded_harnessops_version") != notice.recorded_version:
        return False
    if cache.get("current_harnessops_version") != notice.current_version:
        return False
    last_notice = _parse_time(cache.get("last_notice_at"))
    return last_notice is not None and now - last_notice < NOTICE_INTERVAL


def _compute_update_notice(root: Path) -> UpdateNotice | None:
    if not (root / ".harnessops" / "project.toml").exists():
        return None
    lock = load_lock(root)
    recorded_version = lock.get("harnessops_version")
    if not isinstance(recorded_version, str) or not recorded_version:
        return None
    if not _is_older(recorded_version, __version__):
        return None
    return UpdateNotice(recorded_version=recorded_version, current_version=__version__)


def maybe_emit_update_notice(command_name: str | None) -> None:
    """Best-effort stale HarnessOps notice for ordinary CLI usage."""
    if command_name in SKIPPED_COMMANDS:
        return
    if any(_truthy(os.environ.get(name)) for name in DISABLE_ENV_VARS):
        return

    try:
        root = find_root()
        notice = _compute_update_notice(root)
    except Exception:
        return

    if notice is None:
        return

    now = dt.datetime.now(dt.timezone.utc)
    cache_path = _cache_path(root)
    if _recently_notified(cache_path, notice, now):
        return

    typer.echo(
        "[notice] HarnessOps managed artifacts may be behind current hops: "
        f"{notice.recorded_version} -> {notice.current_version}",
        err=True,
    )
    typer.echo(
        "[notice] Ask the agent to use the `hops-update-harness` skill, "
        "or run: hops update-harness",
        err=True,
    )
    _write_notice_cache(cache_path, notice, now)
