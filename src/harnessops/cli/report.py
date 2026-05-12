from __future__ import annotations

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project


def report_command() -> None:
    """Print a compact HarnessOps repository report."""
    project = load_project(find_root())
    typer.echo(f"profile: {project.profile_id}")
    typer.echo(f"overlay: {project.overlay_path}")


def register(app: typer.Typer) -> None:
    app.command("report")(report_command)

