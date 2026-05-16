from __future__ import annotations

import typer

from harnessops.cli.deprecation import warn_if_deprecated
from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.lab_records import create_decision

STATUSES = {"adopted", "rejected", "parked", "needs-more-evidence", "merged-into-other", "not-upstreamable"}


def decide_command(
    experiment: str | None = typer.Option(None, "--experiment"),
    from_id: str | None = typer.Option(None, "--from"),
    status: str = typer.Option(..., "--status"),
    reason: str = typer.Option("", "--reason"),
    evidence: str = typer.Option("", "--evidence"),
    regression_risk: str = typer.Option("", "--regression-risk"),
    follow_up: str = typer.Option("", "--follow-up"),
    guard_path: str | None = typer.Option(None, "--guard-path"),
) -> None:
    """判断レコードを作成します。"""
    warn_if_deprecated("decide", "hops lab decide")
    if status not in STATUSES:
        typer.echo(f"status が不正です: {status}")
        raise typer.Exit(1)
    source = experiment or from_id
    if not source:
        typer.echo("--experiment または --from を指定してください")
        raise typer.Exit(1)
    if status == "adopted" and (not evidence or not regression_risk or not guard_path):
        typer.echo("adopted の判断には --evidence、--regression-risk、--guard-path が必要です")
        raise typer.Exit(1)
    root = find_root()
    project = load_project(root)
    path = create_decision(
        project,
        source=source,
        status=status,
        title=f"{status} {source}",
        reason=reason or f"`{source}` に対して `{status}` の判断を記録しました。",
        evidence=evidence or "証拠は指定されていません。この判断は採用可能ではありません。",
        regression_risk=regression_risk or "回帰リスクは評価されていません。",
        follow_up=follow_up or "変更を昇格する前にこの判断をレビューしてください。",
        guard_path=guard_path,
    )
    typer.echo(path.relative_to(root).as_posix())


def register(app: typer.Typer) -> None:
    app.command("decide", hidden=True)(decide_command)
