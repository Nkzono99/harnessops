from __future__ import annotations

import typer

from harnessops.core.overlay import GENERATED_MARKER
from harnessops.core.paths import find_root
from harnessops.core.project import load_project


def eval_command(
    case: str = typer.Option(..., "--case"),
    manual: bool = typer.Option(False, "--manual"),
    all_cases: bool = typer.Option(False, "--all"),
    experiment: str | None = typer.Option(None, "--experiment"),
) -> None:
    """Run eval cases or write a manual scoring placeholder."""
    del all_cases, experiment
    root = find_root()
    project = load_project(root)
    view = project.overlay_dir / "views" / f"eval-{case}.md"
    view.parent.mkdir(parents=True, exist_ok=True)
    mode = "manual" if manual else "check"
    view.write_text(GENERATED_MARKER + f"# Eval {case}\n\nmode: {mode}\nstatus: pending-manual-score\n", encoding="utf-8")
    typer.echo(view.relative_to(root).as_posix())


def register(app: typer.Typer) -> None:
    app.command("eval")(eval_command)

