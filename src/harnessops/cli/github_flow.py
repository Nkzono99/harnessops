from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

import typer

from harnessops.core.github_flow import github_flow_policy
from harnessops.core.paths import find_root
from harnessops.core.project import load_project

github_flow_app = typer.Typer(help="target/meta repo 向けの GitHub Flow を実行します。")


def _run(args: list[str], *, cwd: Path) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            args,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return {
            "args": args,
            "returncode": 127,
            "stdout": "",
            "stderr": f"command not found: {args[0]}",
        }
    return {
        "args": args,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _emit(result: dict[str, Any], *, json_output: bool) -> None:
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return
    status = "ok" if result.get("ok") else "failed"
    typer.echo(f"github-flow: {status}")
    if result.get("reason"):
        typer.echo(f"reason: {result['reason']}")
    for item in result.get("commands", []):
        command = " ".join(item.get("args", []))
        typer.echo(f"$ {command}")
        if item.get("stdout", "").strip():
            typer.echo(item["stdout"].rstrip())
        if item.get("stderr", "").strip():
            typer.echo(item["stderr"].rstrip(), err=True)


def _exit(result: dict[str, Any], *, json_output: bool) -> None:
    _emit(result, json_output=json_output)
    if not result.get("ok"):
        raise typer.Exit(1)


def _policy_or_stop(root: Path) -> tuple[dict[str, Any], bool]:
    project = load_project(root)
    policy = github_flow_policy(project)
    result = {
        "ok": policy.enabled,
        "overlay_mode": policy.overlay_mode,
        "base_branch": policy.base_branch,
        "branch_prefix": policy.branch_prefix,
        "require_validation": policy.require_validation,
        "reason": policy.reason,
        "commands": [],
    }
    return result, policy.enabled


def _append_command(result: dict[str, Any], command: dict[str, Any]) -> None:
    result.setdefault("commands", []).append(command)


def _dirty_lines(status_stdout: str) -> list[str]:
    return [
        line
        for line in status_stdout.splitlines()
        if line and not line.startswith("##")
    ]


def _current_branch(root: Path) -> str | None:
    command = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root)
    if command["returncode"] != 0:
        return None
    return str(command["stdout"]).strip()


def _branch_exists(root: Path, branch: str) -> bool:
    command = _run(["git", "rev-parse", "--verify", "--quiet", branch], cwd=root)
    return command["returncode"] == 0


@github_flow_app.command("preflight")
def preflight(
    pull: bool = typer.Option(
        False,
        "--pull",
        help="origin から fetch し、base branch を ff-only pull します。",
    ),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """GitHub Flow 実行前の repo / config / clean worktree を確認します。"""
    root = find_root()
    result, enabled = _policy_or_stop(root)
    result["action"] = "preflight"
    if not enabled:
        _exit(result, json_output=json_output)

    status = _run(["git", "status", "--porcelain=v1", "--branch"], cwd=root)
    _append_command(result, status)
    if status["returncode"] != 0:
        result.update({"ok": False, "reason": "git status failed"})
        _exit(result, json_output=json_output)

    dirty = _dirty_lines(status["stdout"])
    result["dirty"] = dirty
    if dirty:
        result.update({"ok": False, "reason": "worktree is dirty"})
        _exit(result, json_output=json_output)

    if pull:
        fetch = _run(["git", "fetch", "--prune", "origin"], cwd=root)
        _append_command(result, fetch)
        if fetch["returncode"] != 0:
            result.update({"ok": False, "reason": "git fetch failed"})
            _exit(result, json_output=json_output)
        pull_command = _run(
            ["git", "pull", "--ff-only", "origin", result["base_branch"]], cwd=root
        )
        _append_command(result, pull_command)
        if pull_command["returncode"] != 0:
            result.update({"ok": False, "reason": "git pull --ff-only failed"})
            _exit(result, json_output=json_output)

    _exit(result, json_output=json_output)


@github_flow_app.command("publish")
def publish(
    branch: str | None = typer.Option(None, "--branch"),
    message: str = typer.Option("Automated HarnessOps update", "--message", "-m"),
    validation_passed: bool = typer.Option(False, "--validation-passed"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """変更を作業 branch に commit し、origin へ push します。"""
    root = find_root()
    result, enabled = _policy_or_stop(root)
    result["action"] = "publish"
    if not enabled:
        _exit(result, json_output=json_output)
    if result["require_validation"] and not validation_passed:
        result.update({"ok": False, "reason": "--validation-passed is required"})
        _exit(result, json_output=json_output)

    branch = (
        branch
        or f"{result['branch_prefix']}hops-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )
    if not branch.startswith(result["branch_prefix"]):
        branch = f"{result['branch_prefix']}{branch}"
    if branch == result["base_branch"]:
        result.update(
            {"ok": False, "reason": "refusing to publish directly on base branch"}
        )
        _exit(result, json_output=json_output)

    current = _current_branch(root)
    if current != branch:
        switch_args = (
            ["git", "switch", branch]
            if _branch_exists(root, branch)
            else ["git", "switch", "-c", branch]
        )
        switch = _run(switch_args, cwd=root)
        _append_command(result, switch)
        if switch["returncode"] != 0:
            result.update({"ok": False, "reason": "git switch failed"})
            _exit(result, json_output=json_output)

    add = _run(["git", "add", "-A"], cwd=root)
    _append_command(result, add)
    if add["returncode"] != 0:
        result.update({"ok": False, "reason": "git add failed"})
        _exit(result, json_output=json_output)

    diff = _run(["git", "diff", "--cached", "--quiet"], cwd=root)
    if diff["returncode"] == 0:
        result.update({"ok": True, "reason": "no staged changes", "branch": branch})
        _exit(result, json_output=json_output)

    commit = _run(["git", "commit", "-m", message], cwd=root)
    _append_command(result, commit)
    if commit["returncode"] != 0:
        result.update({"ok": False, "reason": "git commit failed"})
        _exit(result, json_output=json_output)

    push = _run(["git", "push", "-u", "origin", "HEAD"], cwd=root)
    _append_command(result, push)
    result.update({"ok": push["returncode"] == 0, "branch": branch})
    if push["returncode"] != 0:
        result["reason"] = "git push failed"
    _exit(result, json_output=json_output)


@github_flow_app.command("pr")
def create_pr(
    base: str | None = typer.Option(None, "--base"),
    title: str | None = typer.Option(None, "--title"),
    body: str | None = typer.Option(None, "--body"),
    body_file: Path | None = typer.Option(None, "--body-file"),
    close_issue: list[str] | None = typer.Option(None, "--close-issue"),
    draft: bool = typer.Option(False, "--draft"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """現在の branch から pull request を作成します。"""
    root = find_root()
    result, enabled = _policy_or_stop(root)
    result["action"] = "pr"
    if not enabled:
        _exit(result, json_output=json_output)

    branch = _current_branch(root)
    title = title or branch or "Automated HarnessOps update"
    body_text = body or ""
    if body_file is not None:
        body_text = body_file.read_text(encoding="utf-8")
    for issue in close_issue or []:
        normalized = issue if issue.startswith("#") else f"#{issue}"
        body_text += f"\n\nCloses {normalized}"

    args = [
        "gh",
        "pr",
        "create",
        "--base",
        base or result["base_branch"],
        "--title",
        title,
        "--body",
        body_text,
    ]
    if draft:
        args.append("--draft")
    command = _run(args, cwd=root)
    _append_command(result, command)
    result["ok"] = command["returncode"] == 0
    if command["returncode"] != 0:
        result["reason"] = "gh pr create failed"
    else:
        result["url"] = command["stdout"].strip()
    _exit(result, json_output=json_output)


@github_flow_app.command("merge")
def merge_pr(
    pr: str | None = typer.Argument(None),
    require_checks: bool = typer.Option(True, "--require-checks/--no-require-checks"),
    delete_branch: bool = typer.Option(True, "--delete-branch/--no-delete-branch"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """PR が conflict なしで merge 可能なら merge します。"""
    root = find_root()
    result, enabled = _policy_or_stop(root)
    result["action"] = "merge"
    if not enabled:
        _exit(result, json_output=json_output)

    target = pr or ""
    view_args = ["gh", "pr", "view"]
    if target:
        view_args.append(target)
    view_args.extend(["--json", "isDraft,mergeStateStatus,state,headRefName"])
    view = _run(view_args, cwd=root)
    _append_command(result, view)
    if view["returncode"] != 0:
        result.update({"ok": False, "reason": "gh pr view failed"})
        _exit(result, json_output=json_output)
    try:
        pr_info = json.loads(view["stdout"])
    except json.JSONDecodeError:
        result.update({"ok": False, "reason": "gh pr view returned invalid JSON"})
        _exit(result, json_output=json_output)

    result["pr"] = pr_info
    if pr_info.get("isDraft"):
        result.update({"ok": False, "reason": "PR is draft"})
        _exit(result, json_output=json_output)
    if pr_info.get("state") != "OPEN":
        result.update(
            {"ok": False, "reason": f"PR is not open: {pr_info.get('state')}"}
        )
        _exit(result, json_output=json_output)
    if pr_info.get("mergeStateStatus") == "DIRTY":
        result.update({"ok": False, "reason": "PR has merge conflicts"})
        _exit(result, json_output=json_output)

    if require_checks:
        checks_args = ["gh", "pr", "checks"]
        if target:
            checks_args.append(target)
        checks_args.append("--required")
        checks = _run(checks_args, cwd=root)
        _append_command(result, checks)
        if checks["returncode"] != 0:
            result.update({"ok": False, "reason": "required checks are not passing"})
            _exit(result, json_output=json_output)

    merge_args = ["gh", "pr", "merge"]
    if target:
        merge_args.append(target)
    merge_args.append("--merge")
    if delete_branch:
        merge_args.append("--delete-branch")
    merge = _run(merge_args, cwd=root)
    _append_command(result, merge)
    result["ok"] = merge["returncode"] == 0
    if merge["returncode"] != 0:
        result["reason"] = "gh pr merge failed"
    _exit(result, json_output=json_output)


def register(app: typer.Typer) -> None:
    app.add_typer(github_flow_app, name="github-flow")
