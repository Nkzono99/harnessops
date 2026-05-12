from __future__ import annotations

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.records import create_decision

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
    """Create a decision record."""
    if status not in STATUSES:
        typer.echo(f"invalid status: {status}")
        raise typer.Exit(1)
    source = experiment or from_id
    if not source:
        typer.echo("provide --experiment or --from")
        raise typer.Exit(1)
    if status == "adopted" and (not evidence or not regression_risk or not guard_path):
        typer.echo("adopted decisions require --evidence, --regression-risk, and --guard-path")
        raise typer.Exit(1)
    root = find_root()
    project = load_project(root)
    path = create_decision(
        project,
        source=source,
        status=status,
        title=f"{status} {source}",
        reason=reason or f"Decision `{status}` recorded for `{source}`.",
        evidence=evidence or "No evidence supplied; this decision is not adoption-ready.",
        regression_risk=regression_risk or "Regression risk not evaluated.",
        follow_up=follow_up or "Review this decision before promoting the change.",
        guard_path=guard_path,
    )
    typer.echo(path.relative_to(root).as_posix())


def register(app: typer.Typer) -> None:
    app.command("decide")(decide_command)
