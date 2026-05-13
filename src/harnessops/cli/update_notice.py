from __future__ import annotations

import datetime as dt
import json
import os
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import typer

from harnessops import __version__
from harnessops.core.lock import load_lock
from harnessops.core.paths import find_root

NOTICE_INTERVAL = dt.timedelta(days=7)
PYPI_CHECK_INTERVAL = dt.timedelta(days=1)
PYPI_JSON_URL = "https://pypi.org/pypi/harnessops/json"
PYPI_TIMEOUT_SECONDS = 1.0
NOTICE_CACHE = "update-notice.json"
DISABLE_ENV_VARS = ("HOPS_DISABLE_UPDATE_NOTICE", "HARNESSOPS_DISABLE_UPDATE_NOTICE")
DISABLE_PYPI_ENV_VARS = ("HOPS_DISABLE_PYPI_UPDATE_CHECK", "HARNESSOPS_DISABLE_PYPI_UPDATE_CHECK")
SKIPPED_COMMANDS = {"update-harness", "version"}

UPDATE_COMMAND = "uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge"
DOCTOR_COMMAND = "uvx --from harnessops hops doctor --check-overlay --check-records"
MIGRATE_CHECK_COMMAND = "uvx --from harnessops hops migrate --check"


@dataclass(frozen=True)
class UpdateNotice:
    recorded_version: str
    current_version: str
    latest_version: str | None = None


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


def _write_cache(path: Path, payload: dict[str, object]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError:
        return


def _write_notice_cache(path: Path, notice: UpdateNotice, now: dt.datetime) -> None:
    payload = _load_notice_cache(path)
    payload.update(
        {
            "schema_version": "0.2",
            "kind": "harnessops_update_notice",
            "last_notice_at": now.isoformat(),
            "recorded_harnessops_version": notice.recorded_version,
            "current_harnessops_version": notice.current_version,
            "latest_harnessops_version": notice.latest_version,
        }
    )
    _write_cache(path, payload)


def _write_pypi_cache(path: Path, latest_version: str | None, now: dt.datetime) -> None:
    payload = _load_notice_cache(path)
    payload.update(
        {
            "schema_version": "0.2",
            "kind": "harnessops_update_notice",
            "last_pypi_check_at": now.isoformat(),
        }
    )
    if latest_version is not None:
        payload["latest_harnessops_version"] = latest_version
    _write_cache(path, payload)


def _fetch_latest_pypi_version() -> str | None:
    request = urllib.request.Request(
        PYPI_JSON_URL,
        headers={
            "Accept": "application/json",
            "User-Agent": f"harnessops/{__version__}",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=PYPI_TIMEOUT_SECONDS) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:  # noqa: BLE001
        return None

    info = payload.get("info")
    if not isinstance(info, dict):
        return None
    version = info.get("version")
    return version if isinstance(version, str) and version else None


def _cached_pypi_latest(cache: dict[str, object], now: dt.datetime) -> tuple[str | None, bool]:
    last_checked = _parse_time(cache.get("last_pypi_check_at"))
    latest = cache.get("latest_harnessops_version")
    latest_version = latest if isinstance(latest, str) and latest else None
    if last_checked is None:
        return latest_version, False
    return latest_version, now - last_checked < PYPI_CHECK_INTERVAL


def _resolve_latest_pypi_version(root: Path, now: dt.datetime) -> str | None:
    cache_path = _cache_path(root)
    cache = _load_notice_cache(cache_path)
    cached_latest, cache_is_fresh = _cached_pypi_latest(cache, now)
    if cache_is_fresh:
        return cached_latest
    if any(_truthy(os.environ.get(name)) for name in DISABLE_PYPI_ENV_VARS):
        return cached_latest

    latest = _fetch_latest_pypi_version()
    _write_pypi_cache(cache_path, latest, now)
    return latest or cached_latest


def _versions_need_notice(recorded: str, current: str, latest: str | None) -> bool:
    if _is_older(recorded, current) or _is_older(current, recorded):
        return True
    if latest and (_is_older(recorded, latest) or _is_older(current, latest)):
        return True
    return False


def _format_notice(notice: UpdateNotice) -> list[str]:
    latest = notice.latest_version or "unknown"
    return [
        "[notice] HarnessOps update path available:",
        f"[notice]   repo managed artifacts: {notice.recorded_version}",
        f"[notice]   current hops runtime:   {notice.current_version}",
        f"[notice]   latest PyPI release:    {latest}",
        "[notice] To update this repo through the uvx HarnessOps path:",
        f"[notice]   {UPDATE_COMMAND}",
        "[notice] Then verify without applying migrations automatically:",
        f"[notice]   {DOCTOR_COMMAND}",
        f"[notice]   {MIGRATE_CHECK_COMMAND}",
    ]


def _recently_notified(path: Path, notice: UpdateNotice, now: dt.datetime) -> bool:
    cache = _load_notice_cache(path)
    if cache.get("recorded_harnessops_version") != notice.recorded_version:
        return False
    if cache.get("current_harnessops_version") != notice.current_version:
        return False
    if cache.get("latest_harnessops_version") != notice.latest_version:
        return False
    last_notice = _parse_time(cache.get("last_notice_at"))
    return last_notice is not None and now - last_notice < NOTICE_INTERVAL


def _compute_update_notice(root: Path, now: dt.datetime | None = None) -> UpdateNotice | None:
    if not (root / ".harnessops" / "project.toml").exists():
        return None
    lock = load_lock(root)
    recorded_version = lock.get("harnessops_version")
    if not isinstance(recorded_version, str) or not recorded_version:
        return None

    check_time = now or dt.datetime.now(dt.timezone.utc)
    latest_version = _resolve_latest_pypi_version(root, check_time)
    if not _versions_need_notice(recorded_version, __version__, latest_version):
        return None
    return UpdateNotice(
        recorded_version=recorded_version,
        current_version=__version__,
        latest_version=latest_version,
    )


def maybe_emit_update_notice(command_name: str | None) -> None:
    """Best-effort HarnessOps update notice for ordinary CLI usage."""
    if command_name in SKIPPED_COMMANDS:
        return
    if any(_truthy(os.environ.get(name)) for name in DISABLE_ENV_VARS):
        return

    try:
        root = find_root()
        now = dt.datetime.now(dt.timezone.utc)
        notice = _compute_update_notice(root, now=now)
    except Exception:
        return

    if notice is None:
        return

    cache_path = _cache_path(root)
    if _recently_notified(cache_path, notice, now):
        return

    for line in _format_notice(notice):
        typer.echo(line, err=True)
    _write_notice_cache(cache_path, notice, now)
