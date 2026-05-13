from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from packaging.version import InvalidVersion, Version

from harnessops import __version__
from harnessops.core.lock import load_lock

PYPI_JSON_URL = "https://pypi.org/pypi/harnessops/json"
PYPI_TIMEOUT_SECONDS = 2.0
CHAIN_ACTIVE_ENV = "HOPS_UPGRADE_CHAIN_ACTIVE"
GRANULARITIES = {"patch", "minor", "major"}


@dataclass(frozen=True)
class UpgradeStep:
    version: str
    command: list[str]


@dataclass(frozen=True)
class UpgradePlan:
    recorded_version: str | None
    current_version: str
    target_version: str
    latest_pypi_version: str | None
    granularity: str
    steps: list[UpgradeStep]
    available_versions: list[str]
    reason: str | None = None

    @property
    def needed(self) -> bool:
        return bool(self.steps)

    def as_dict(self) -> dict[str, object]:
        return {
            "recorded_version": self.recorded_version,
            "current_version": self.current_version,
            "target_version": self.target_version,
            "latest_pypi_version": self.latest_pypi_version,
            "granularity": self.granularity,
            "needed": self.needed,
            "reason": self.reason,
            "steps": [
                {"version": step.version, "command": " ".join(step.command)}
                for step in self.steps
            ],
        }


@dataclass(frozen=True)
class UpgradeRun:
    version: str
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    def as_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "command": " ".join(self.command),
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


def parsed_version(value: str) -> Version | None:
    try:
        return Version(value)
    except InvalidVersion:
        return None


def is_older(left: str, right: str) -> bool:
    left_version = parsed_version(left)
    right_version = parsed_version(right)
    if left_version is None or right_version is None:
        return left != right and left < right
    return left_version < right_version


def fetch_pypi_versions() -> tuple[list[str], str | None]:
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
        return [], None

    releases = payload.get("releases")
    versions = list(releases) if isinstance(releases, dict) else []
    info = payload.get("info")
    latest = None
    if isinstance(info, dict) and isinstance(info.get("version"), str):
        latest = info["version"]
    return versions, latest


def _stable_sorted_versions(values: list[str], *, include_prerelease: bool) -> list[str]:
    parsed: list[tuple[Version, str]] = []
    for value in values:
        version = parsed_version(value)
        if version is None:
            continue
        if version.is_prerelease and not include_prerelease:
            continue
        parsed.append((version, value))
    parsed.sort(key=lambda item: item[0])
    return [value for _, value in parsed]


def _version_key(version: Version, granularity: str) -> tuple[int, ...]:
    if granularity == "patch":
        return tuple(version.release)
    if granularity == "major":
        return (version.major,)
    return (version.major, version.minor)


def _checkpoint_versions(
    *,
    recorded: str,
    target: str,
    available_versions: list[str],
    granularity: str,
) -> list[str]:
    recorded_version = parsed_version(recorded)
    target_version = parsed_version(target)
    if recorded_version is None or target_version is None or recorded_version >= target_version:
        return []

    include_prerelease = target_version.is_prerelease
    candidates = _stable_sorted_versions(available_versions + [target], include_prerelease=include_prerelease)
    selected: dict[tuple[int, ...], tuple[Version, str]] = {}
    for candidate in candidates:
        parsed = parsed_version(candidate)
        if parsed is None or parsed <= recorded_version or parsed > target_version:
            continue
        key = _version_key(parsed, granularity)
        previous = selected.get(key)
        if previous is None or previous[0] < parsed:
            selected[key] = (parsed, candidate)

    checkpoints = sorted(selected.values(), key=lambda item: item[0])
    return [value for _, value in checkpoints]


def _step_command(version: str, extra_args: list[str] | None = None) -> list[str]:
    command = ["uvx", "--from", f"harnessops=={version}", "hops", "update-harness"]
    if extra_args:
        command.extend(extra_args)
    return command


def build_upgrade_plan(
    root: Path,
    *,
    target_version: str | None = None,
    granularity: str = "minor",
    extra_args: list[str] | None = None,
    intermediate_args: list[str] | None = None,
    pypi_versions: list[str] | None = None,
    latest_pypi_version: str | None = None,
) -> UpgradePlan:
    if granularity not in GRANULARITIES:
        raise ValueError(f"unknown upgrade granularity: {granularity}")

    lock = load_lock(root)
    recorded = lock.get("harnessops_version")
    if not isinstance(recorded, str) or not recorded:
        return UpgradePlan(
            recorded_version=None,
            current_version=__version__,
            target_version=target_version or __version__,
            latest_pypi_version=latest_pypi_version,
            granularity=granularity,
            steps=[],
            available_versions=[],
            reason="lock has no harnessops_version",
        )

    target = target_version or __version__
    if not is_older(recorded, target):
        return UpgradePlan(
            recorded_version=recorded,
            current_version=__version__,
            target_version=target,
            latest_pypi_version=latest_pypi_version,
            granularity=granularity,
            steps=[],
            available_versions=[],
            reason="recorded version is already at or ahead of target",
        )

    if pypi_versions is None:
        pypi_versions, fetched_latest = fetch_pypi_versions()
        latest_pypi_version = latest_pypi_version or fetched_latest

    checkpoints = _checkpoint_versions(
        recorded=recorded,
        target=target,
        available_versions=pypi_versions,
        granularity=granularity,
    )
    steps = [
        UpgradeStep(
            version=version,
            command=_step_command(
                version,
                extra_args if version == target else intermediate_args if intermediate_args is not None else extra_args,
            ),
        )
        for version in checkpoints
    ]
    reason = None if steps else "no usable PyPI checkpoint versions found"
    return UpgradePlan(
        recorded_version=recorded,
        current_version=__version__,
        target_version=target,
        latest_pypi_version=latest_pypi_version,
        granularity=granularity,
        steps=steps,
        available_versions=_stable_sorted_versions(pypi_versions, include_prerelease=False),
        reason=reason,
    )


def upgrade_chain_active() -> bool:
    return os.environ.get(CHAIN_ACTIVE_ENV) == "1"


def run_upgrade_step(step: UpgradeStep, *, cwd: Path) -> UpgradeRun:
    env = os.environ.copy()
    env[CHAIN_ACTIVE_ENV] = "1"
    completed = subprocess.run(  # noqa: S603
        step.command,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    return UpgradeRun(
        version=step.version,
        command=step.command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def run_upgrade_chain(plan: UpgradePlan, *, cwd: Path) -> list[UpgradeRun]:
    runs: list[UpgradeRun] = []
    for step in plan.steps:
        run = run_upgrade_step(step, cwd=cwd)
        runs.append(run)
        if run.returncode != 0:
            break
    return runs
