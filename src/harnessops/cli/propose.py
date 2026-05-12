from __future__ import annotations

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.records import create_hypothesis, find_record, read_record


def propose_command(
    from_id: str = typer.Option(..., "--from"),
    manual_template: bool = typer.Option(True, "--manual-template/--agent-assisted"),
) -> None:
    """Scaffold an improvement hypothesis from an eval case."""
    if not manual_template:
        typer.echo("agent-assisted mode is not implemented in MVP; writing manual template")
    root = find_root()
    project = load_project(root)
    eval_path = find_record(project, from_id)
    frontmatter, _ = read_record(eval_path)
    path = create_hypothesis(
        project,
        eval_case_id=str(frontmatter.get("id", from_id)),
        title=f"Hypothesis for {eval_path.stem}",
        capability=str(frontmatter.get("capability", "unclassified")),
    )
    typer.echo(path.relative_to(root).as_posix())


def register(app: typer.Typer) -> None:
    app.command("propose")(propose_command)

