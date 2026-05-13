from __future__ import annotations

import json

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.steward import steward_finalize, steward_preflight


steward_app = typer.Typer(help="daily steward の定型 preflight と run ledger を作成します。")


@steward_app.command("preflight")
def preflight_command(
    pull: bool = typer.Option(
        False,
        "--pull/--no-pull",
        help="clean worktree の場合だけ git fetch --prune と git pull --ff-only を実行します。",
    ),
    check_records: bool = typer.Option(
        True,
        "--check-records/--no-check-records",
        help="doctor 相当の record validation も実行します。",
    ),
    json_output: bool = typer.Option(False, "--json", help="機械可読JSONで出力します。"),
) -> None:
    """daily steward automation の deterministic preflight を実行します。"""
    project = load_project(find_root())
    result = steward_preflight(project, pull=pull, check_records=check_records)
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        typer.echo(f"mode: {result['mode']}")
        typer.echo(f"repo: {result['project']['name']} ({result['project']['kind']})")
        typer.echo(f"pull_status: {result['git']['pull_status']}")
        typer.echo(f"can_continue: {str(result['can_continue']).lower()}")
        typer.echo(f"doctor: {result['doctor'].get('ok')}")
        typer.echo(f"migration: {result['migration'].get('ok')}")
        triggered = [
            lane for lane, data in result["lane_triggers"].items() if data["triggered"]
        ]
        typer.echo(f"triggered_lanes: {', '.join(triggered) if triggered else 'none'}")
        typer.echo(f"next: {result['next_agent_step']}")
    if not result["ok"]:
        raise typer.Exit(1)


@steward_app.command("finalize")
def finalize_command(
    policy: str = typer.Option(
        "patch-only",
        "--policy",
        help="run 後の変更処理。patch-only または commit-local。",
    ),
    validation_passed: bool = typer.Option(
        False,
        "--validation-passed",
        help="commit-local を許可する前に validation が通ったことを明示します。",
    ),
    branch: str | None = typer.Option(
        None,
        "--branch",
        help="commit-local で作成する local branch 名。省略時は codex/steward/* を生成します。",
    ),
    branch_prefix: str = typer.Option(
        "codex/steward",
        "--branch-prefix",
        help="branch 未指定時の automation branch prefix。",
    ),
    message: str = typer.Option(
        "hops daily steward local advance",
        "--message",
        help="commit-local で使う commit message。",
    ),
    json_output: bool = typer.Option(False, "--json", help="機械可読JSONで出力します。"),
) -> None:
    """daily steward run 後の patch-only / commit-local 処理を行います。"""
    project = load_project(find_root())
    try:
        result = steward_finalize(
            project,
            policy=policy,
            validation_passed=validation_passed,
            branch=branch,
            branch_prefix=branch_prefix,
            message=message,
        )
    except (RuntimeError, ValueError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        typer.echo(f"policy: {result['policy']}")
        typer.echo(f"status: {result.get('status', 'error')}")
        typer.echo(f"branch: {result.get('branch_after')}")
        typer.echo(f"commit: {result.get('commit_hash') or 'none'}")
        typer.echo(f"can_continue_next_run: {str(result.get('can_continue_next_run')).lower()}")
        if result.get("changed_files"):
            typer.echo("changed_files:")
            for item in result["changed_files"]:
                typer.echo(f"- {item}")
        if result.get("next"):
            typer.echo(f"next: {result['next']}")
    if not result["ok"]:
        raise typer.Exit(1)


def register(app: typer.Typer) -> None:
    app.add_typer(steward_app, name="steward")
