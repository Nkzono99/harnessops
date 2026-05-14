from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from harnessops.core.project import Project


GITHUB_FLOW_CAPABLE_MODES = {"upstream-lab", "meta-lab"}
DEFAULT_BASE_BRANCH = "main"
DEFAULT_BRANCH_PREFIX = "codex/"


@dataclass(frozen=True)
class GitHubFlowPolicy:
    enabled: bool
    capable: bool
    overlay_mode: str | None
    base_branch: str
    branch_prefix: str
    require_validation: bool
    reason: str | None = None


def default_github_flow_enabled(overlay_mode: str | None) -> bool:
    return overlay_mode in GITHUB_FLOW_CAPABLE_MODES


def default_github_flow_config(
    overlay_mode: str | None, *, enabled: bool | None = None
) -> dict[str, Any]:
    resolved_enabled = (
        default_github_flow_enabled(overlay_mode) if enabled is None else enabled
    )
    return {
        "enabled": resolved_enabled,
        "base_branch": DEFAULT_BASE_BRANCH,
        "branch_prefix": DEFAULT_BRANCH_PREFIX,
        "require_validation": True,
    }


def github_flow_policy(
    project: Project, *, enabled_override: bool | None = None
) -> GitHubFlowPolicy:
    config = dict(default_github_flow_config(project.overlay_mode))
    raw_config = project.data.get("github_flow")
    if isinstance(raw_config, dict):
        config.update(raw_config)
    if enabled_override is not None:
        config["enabled"] = enabled_override

    capable = project.overlay_mode in GITHUB_FLOW_CAPABLE_MODES
    enabled = (
        bool(config.get("enabled", default_github_flow_enabled(project.overlay_mode)))
        and capable
    )
    reason = None
    if not capable:
        reason = f"overlay_mode={project.overlay_mode!r} is not a target/meta harness repository"
    elif not bool(config.get("enabled", True)):
        reason = "github_flow.enabled is false"

    return GitHubFlowPolicy(
        enabled=enabled,
        capable=capable,
        overlay_mode=project.overlay_mode,
        base_branch=str(config.get("base_branch") or DEFAULT_BASE_BRANCH),
        branch_prefix=str(config.get("branch_prefix") or DEFAULT_BRANCH_PREFIX),
        require_validation=bool(config.get("require_validation", True)),
        reason=reason,
    )
