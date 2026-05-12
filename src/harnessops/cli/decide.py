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
) -> None:
    """Create a decision record."""
    if status not in STATUSES:
        typer.echo(f"invalid status: {status}")
        raise typer.Exit(1)
    source = experiment or from_id
    if not source:
        typer.echo("provide --experiment or --from")
        raise typer.Exit(1)
    root = find_root()
    project = load_project(root)
    path = create_decision(project, source=source, status=status, title=f"{status} {source}")
    typer.echo(path.relative_to(root).as_posix())


def register(app: typer.Typer) -> None:
    app.command("decide")(decide_command)

