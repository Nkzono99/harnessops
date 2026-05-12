from __future__ import annotations

import typer

from harnessops.core.evaluation import parse_scores, write_manual_eval
from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.records import find_record, read_record


def eval_command(
    case: str | None = typer.Option(None, "--case"),
    manual: bool = typer.Option(False, "--manual"),
    all_cases: bool = typer.Option(False, "--all"),
    experiment: str | None = typer.Option(None, "--experiment"),
    score: list[str] = typer.Option(None, "--score"),
    notes: str = typer.Option("", "--notes"),
) -> None:
    """Persist manual multi-axis scorecards for eval cases."""
    root = find_root()
    project = load_project(root)
    cases = []
    if all_cases:
        cases = [path.stem.split("-", 1)[0] for path in sorted((project.overlay_dir / "records/eval-cases").glob("E*.md"))]
    elif experiment:
        try:
            experiment_path = find_record(project, experiment)
            frontmatter, _ = read_record(experiment_path)
            cases = [str(item) for item in frontmatter.get("eval_cases", [])]
        except FileNotFoundError:
            typer.echo(f"experiment not found: {experiment}")
            raise typer.Exit(1)
    elif case:
        cases = [case]
    else:
        typer.echo("provide --case or --all")
        raise typer.Exit(1)
    if not cases:
        typer.echo("no eval cases found")
        raise typer.Exit(1)
    if not manual:
        typer.echo("manual scoring is required for this command; pass --manual")
        raise typer.Exit(1)
    try:
        scores = parse_scores(score or [])
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    outputs = []
    for case_id in cases:
        yml_path, md_path = write_manual_eval(project, case_id=case_id, scores=scores, notes=notes, experiment=experiment)
        outputs.append(yml_path.relative_to(root).as_posix())
        outputs.append(md_path.relative_to(root).as_posix())
    typer.echo("\n".join(outputs))


def register(app: typer.Typer) -> None:
    app.command("eval")(eval_command)
