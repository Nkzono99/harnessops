from __future__ import annotations

import json

import typer

from harnessops.core.migration import apply_migrations, check_migrations
from harnessops.core.paths import find_root
from harnessops.core.project import load_project


def migrate_command(
    check: bool = typer.Option(False, "--check"),
    apply: bool = typer.Option(False, "--apply"),  # noqa: A002
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Check or apply HarnessOps layout migrations."""
    project = load_project(find_root())
    if apply:
        entry = apply_migrations(project)
        result = {"ok": True, "pending": [], "entry": str(entry) if entry else None}
    else:
        del check
        result = check_migrations(project)
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))
    else:
        typer.echo("no pending migrations" if result["ok"] else "pending migrations")
        for item in result.get("pending", []):
            typer.echo(item)
    if not result["ok"]:
        raise typer.Exit(1)


def register(app: typer.Typer) -> None:
    app.command("migrate")(migrate_command)
