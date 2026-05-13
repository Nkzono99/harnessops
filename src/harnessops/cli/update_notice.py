from __future__ import annotations

import datetime as dt
import json
import os
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from packaging.version import InvalidVersion, Version
import typer

from harnessops import __version__
from harnessops.core.lock import load_lock
from harnessops.core.paths import find_root

NOTICE_INTERVAL = dt.timedelta(days=7)
PYPI_CHECK_INTERVAL = dt.timedelta(days=1)
PYPI_FAILURE_CHECK_INTERVAL = dt.timedelta(hours=1)
PYPI_JSON_URL = "https://pypi.org/pypi/harnessops/json"
PYPI_TIMEOUT_SECONDS = 1.0
NOTICE_CACHE = "update-notice.json"
DISABLE_ENV_VARS = ("HOPS_DISABLE_UPDATE_NOTICE", "HARNESSOPS_DISABLE_UPDATE_NOTICE")
DISABLE_PYPI_ENV_VARS = ("HOPS_DISABLE_PYPI_UPDATE_CHECK", "HARNESSOPS_DISABLE_PYPI_UPDATE_CHECK")
SKIPPED_COMMANDS = {"update-harness", "version"}

UPDATE_COMMAND = "uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge"
DOCTOR_COMMAND = "uvx --from harnessops hops doctor --check-overlay --check-records"
MIGRATE_CHECK_COMMAND = "uvx --from harnessops hops migrate --check"
LOCAL_UPDATE_COMMAND = "hops update-harness --agent-bridge"
EDITABLE_UPDATE_COMMAND = "uv run --with-editable <harnessops-checkout> hops update-harness --agent-bridge"


def _pinned_update_command(version: str) -> str:
    return f"uvx --from harnessops=={version} hops update-harness --agent-bridge"


@dataclass(frozen=True)
class UpdateNotice:
    recorded_version: str
    current_version: str
    latest_version: str | None = None


def _truthy(value: str | None) -> bool:
    return value is not None and value.strip().lower() in {"1", "true", "yes", "on"}


def _version(value: str) -> Version | None:
    try:
        return Version(value)
    except InvalidVersion:
        return None


def _is_older(recorded: str, current: str) -> bool:
    recorded_version = _version(recorded)
    current_version = _version(current)
    if recorded_version is None or current_version is None:
        return recorded != current and recorded < current
    return recorded_version < current_version


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
            "last_pypi_success_at": now.isoformat(),
        }
    )
    if latest_version is not None:
        payload["latest_harnessops_version"] = latest_version
    _write_cache(path, payload)


def _write_pypi_failure_cache(path: Path, now: dt.datetime) -> None:
    payload = _load_notice_cache(path)
    payload.update(
        {
            "schema_version": "0.2",
            "kind": "harnessops_update_notice",
            "last_pypi_failure_at": now.isoformat(),
        }
    )
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
    latest = cache.get("latest_harnessops_version")
    latest_version = latest if isinstance(latest, str) and latest else None
    last_success = _parse_time(cache.get("last_pypi_success_at"))
    if last_success is None and latest_version is not None:
        last_success = _parse_time(cache.get("last_pypi_check_at"))
    if last_success is None:
        return latest_version, False
    return latest_version, now - last_success < PYPI_CHECK_INTERVAL


def _recent_pypi_failure(cache: dict[str, object], now: dt.datetime) -> bool:
    last_failure = _parse_time(cache.get("last_pypi_failure_at"))
    return last_failure is not None and now - last_failure < PYPI_FAILURE_CHECK_INTERVAL


def _resolve_latest_pypi_version(root: Path, now: dt.datetime) -> str | None:
    cache_path = _cache_path(root)
    cache = _load_notice_cache(cache_path)
    cached_latest, cache_is_fresh = _cached_pypi_latest(cache, now)
    if cache_is_fresh:
        return cached_latest
    if any(_truthy(os.environ.get(name)) for name in DISABLE_PYPI_ENV_VARS):
        return cached_latest
    if _recent_pypi_failure(cache, now):
        return cached_latest

    latest = _fetch_latest_pypi_version()
    if latest is None:
        _write_pypi_failure_cache(cache_path, now)
        return cached_latest
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
    lines = [
        "[notice] HarnessOps update path available:",
        f"[notice]   repo managed artifacts: {notice.recorded_version}",
        f"[notice]   current hops runtime:   {notice.current_version}",
        f"[notice]   latest PyPI release:    {latest}",
    ]
    if _is_older(notice.current_version, notice.recorded_version):
        if notice.latest_version and _is_older(notice.latest_version, notice.recorded_version):
            lines.extend(
                [
                    "[notice] This repo was last updated by a newer HarnessOps runtime than the current one.",
                    "[notice] The latest PyPI release is older than this repo's managed artifacts.",
                    "[notice] If the recorded version is published and intentional, run it explicitly:",
                    f"[notice]   {_pinned_update_command(notice.recorded_version)}",
                    "[notice] If it came from an unreleased checkout, publish it before target/project uvx updates or apply the same checkout locally:",
                    f"[notice]   {EDITABLE_UPDATE_COMMAND}",
                ]
            )
        else:
            lines.extend(
                [
                    "[notice] This repo was last updated by a newer HarnessOps runtime than the current one.",
                    "[notice] Use the uvx latest path, or run the recorded HarnessOps version if it is intentionally pinned:",
                    f"[notice]   {UPDATE_COMMAND}",
                ]
            )
    elif notice.latest_version and _is_older(notice.current_version, notice.latest_version):
        lines.extend(
            [
                "[notice] To update this repo through the uvx HarnessOps path:",
                f"[notice]   {UPDATE_COMMAND}",
            ]
        )
    elif notice.latest_version and _is_older(notice.latest_version, notice.current_version):
        lines.extend(
            [
                "[notice] The current hops runtime is newer than the latest PyPI release.",
                "[notice] If this is an unreleased checkout, apply it with the current runtime:",
                f"[notice]   {LOCAL_UPDATE_COMMAND}",
                "[notice] To keep target/project repos on the uvx path, publish or wait for the PyPI release first.",
            ]
        )
    else:
        lines.extend(
            [
                "[notice] To update this repo through the uvx HarnessOps path:",
                f"[notice]   {UPDATE_COMMAND}",
            ]
        )
    lines.extend(
        [
            "[notice] Then verify without applying migrations automatically:",
            f"[notice]   {DOCTOR_COMMAND}",
            f"[notice]   {MIGRATE_CHECK_COMMAND}",
        ]
    )
    return lines


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
