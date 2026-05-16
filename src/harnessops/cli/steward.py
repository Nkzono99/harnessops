from __future__ import annotations

import json
from pathlib import Path
import sys

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.steward import (
    steward_finalize,
    steward_preflight,
    steward_record_lane_result,
    steward_run_end,
    steward_run_start,
    validate_lane_result,
)


steward_app = typer.Typer(help="daily steward の定型 preflight と run ledger を作成します。")
run_app = typer.Typer(help="daily steward run ledger を操作します。")


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
    update_policy: str = typer.Option(
        "signal-only",
        "--update-policy",
        help="supervisor plan に渡す update policy。signal-only または apply。",
    ),
    json_output: bool = typer.Option(False, "--json", help="機械可読JSONで出力します。"),
) -> None:
    """daily steward automation の deterministic preflight を実行します。"""
    project = load_project(find_root())
    try:
        result = steward_preflight(
            project,
            pull=pull,
            check_records=check_records,
            update_policy=update_policy,
        )
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        typer.echo(f"mode: {result['mode']}")
        typer.echo(f"repo: {result['project']['name']} ({result['project']['kind']})")
        typer.echo(f"pull_status: {result['git']['pull_status']}")
        typer.echo(f"can_continue: {str(result['can_continue']).lower()}")
        typer.echo(f"doctor: {result['doctor'].get('ok')}")
        typer.echo(f"migration: {result['migration'].get('ok')}")
        lab_health = result["lab_health"]
        if lab_health.get("available"):
            typer.echo(f"lab_health: {lab_health.get('status')} ({lab_health.get('reason')})")
        else:
            typer.echo(f"lab_health: unavailable ({lab_health.get('reason')})")
        triggered = [
            lane for lane, data in result["lane_triggers"].items() if data["triggered"]
        ]
        typer.echo(f"triggered_lanes: {', '.join(triggered) if triggered else 'none'}")
        supervisor_lanes = [
            f"{lane['order']}:{lane['skill']}"
            for lane in result["supervisor_plan"]["lanes"]
        ]
        typer.echo(f"supervisor_lanes: {', '.join(supervisor_lanes)}")
        typer.echo(f"next: {result['next_agent_step']}")
    if not result["ok"]:
        raise typer.Exit(1)


def _load_json_input(result_json: str | None, result_file: Path | None) -> object:
    if result_json and result_file:
        raise ValueError("--result-json and --result-file cannot be used together")
    if result_json:
        text = result_json
    elif result_file:
        text = result_file.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    if not text.strip():
        raise ValueError("lane result JSON is required")
    return json.loads(text)


@run_app.command("start")
def run_start_command(
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
    update_policy: str = typer.Option(
        "signal-only",
        "--update-policy",
        help="supervisor plan に渡す update policy。signal-only または apply。",
    ),
    json_output: bool = typer.Option(False, "--json", help="機械可読JSONで出力します。"),
) -> None:
    """preflight を実行し、daily steward run ledger を開始します。"""
    project = load_project(find_root())
    try:
        result = steward_run_start(
            project,
            pull=pull,
            check_records=check_records,
            update_policy=update_policy,
        )
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        typer.echo(f"run_id: {result['run_id']}")
        typer.echo(f"path: {result['path']}")
        typer.echo(f"can_continue: {str(result['preflight']['can_continue']).lower()}")
        typer.echo(f"update_policy: {result['supervisor_plan']['update_policy']}")
    if not result["ok"]:
        raise typer.Exit(1)


@run_app.command("validate-lane-result")
def run_validate_lane_result_command(
    result_json: str | None = typer.Option(None, "--result-json", help="lane result JSON 文字列。"),
    result_file: Path | None = typer.Option(None, "--result-file", help="lane result JSON file。"),
    json_output: bool = typer.Option(False, "--json", help="機械可読JSONで出力します。"),
) -> None:
    """lane result が supervisor contract を満たすか検証します。"""
    try:
        result = validate_lane_result(_load_json_input(result_json, result_file))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        typer.echo(f"ok: {str(result['ok']).lower()}")
        if result["errors"]:
            typer.echo("errors:")
            for error in result["errors"]:
                typer.echo(f"- {error}")
    if not result["ok"]:
        raise typer.Exit(1)


@run_app.command("record-lane-result")
def run_record_lane_result_command(
    run_id: str = typer.Option(..., "--run-id", help="run start で作成した run id。"),
    lane: str = typer.Option(..., "--lane", help="lane 名または skill 名。"),
    result_json: str | None = typer.Option(None, "--result-json", help="lane result JSON 文字列。"),
    result_file: Path | None = typer.Option(None, "--result-file", help="lane result JSON file。"),
    json_output: bool = typer.Option(False, "--json", help="機械可読JSONで出力します。"),
) -> None:
    """lane result を検証し、run ledger に記録します。"""
    project = load_project(find_root())
    try:
        result_data = _load_json_input(result_json, result_file)
        if not isinstance(result_data, dict):
            raise ValueError("lane result must be a JSON object")
        result = steward_record_lane_result(
            project,
            run_id=run_id,
            lane=lane,
            result=result_data,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        typer.echo(f"ok: {str(result['ok']).lower()}")
        typer.echo(f"run_id: {run_id}")
        typer.echo(f"lane: {lane}")
        if result.get("status"):
            typer.echo(f"status: {result['status']}")
        if result.get("error"):
            typer.echo(f"error: {result['error']}")
    if not result["ok"]:
        raise typer.Exit(1)


@run_app.command("end")
def run_end_command(
    run_id: str = typer.Option(..., "--run-id", help="run start で作成した run id。"),
    status: str = typer.Option(..., "--status", help="completed / blocked / failed-validation / no-op。"),
    json_output: bool = typer.Option(False, "--json", help="機械可読JSONで出力します。"),
) -> None:
    """daily steward run ledger を終了します。"""
    project = load_project(find_root())
    try:
        result = steward_run_end(project, run_id=run_id, status=status)
    except (OSError, ValueError, FileNotFoundError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        typer.echo(f"ok: {str(result['ok']).lower()}")
        typer.echo(f"run_id: {run_id}")
        typer.echo(f"status: {status}")
        if result.get("pending_lanes"):
            typer.echo("pending_lanes:")
            for lane in result["pending_lanes"]:
                typer.echo(f"- {lane}")
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
    steward_app.add_typer(run_app, name="run")
    app.add_typer(steward_app, name="steward")
