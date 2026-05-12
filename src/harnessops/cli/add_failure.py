from __future__ import annotations

from typing import Optional

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.records import create_failure
from harnessops.core.render import refresh_views
from harnessops.core.routing import classify_text


def add_failure_command(
    title: str = typer.Option(..., "--title"),
    target: Optional[str] = typer.Option(None, "--target"),
    context: str = typer.Option("", "--context"),
    what_happened: str = typer.Option("", "--what-happened"),
    why_matters: str = typer.Option("", "--why-matters"),
    desired_behavior: str = typer.Option("", "--desired-behavior"),
    local_workaround: str = typer.Option("", "--local-workaround"),
    disposition: Optional[str] = typer.Option(None, "--disposition"),
    from_file: Optional[str] = typer.Option(None, "--from-file"),
    interactive: bool = typer.Option(False, "--interactive"),
) -> None:
    """Create a project-side failure record."""
    del interactive
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"feedback-source", "local-and-feedback"}:
        typer.echo("add-failure requires feedback-source or local-and-feedback mode")
        raise typer.Exit(1)
    file_text = ""
    if from_file:
        file_text = (root / from_file).read_text(encoding="utf-8")
    routing = classify_text(" ".join([title, context, what_happened, file_text]), target=target)
    path = create_failure(
        project,
        title=title,
        target=target,
        context=context or file_text,
        what_happened=what_happened or file_text,
        why_matters=why_matters,
        desired_behavior=desired_behavior,
        local_workaround=local_workaround,
        disposition_type=disposition or routing["type"],
    )
    refresh_views(root, project.overlay_path)
    typer.echo(path.relative_to(root).as_posix())


def add_feedback_command() -> None:
    """Create a feedback draft from an existing failure.

    MVP keeps explicit feedback generation in `hops feedback export`.
    """
    typer.echo("Use `hops feedback export --target <target> --sanitize` to create feedback bundles.")


def register(app: typer.Typer) -> None:
    app.command("add-failure")(add_failure_command)
    app.command("add-feedback")(add_feedback_command)

