from __future__ import annotations

from pathlib import Path

import typer

from harnessops.cli.feedback import import_feedback
from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.records import create_eval_case, find_record, read_record
from harnessops.core.render import refresh_views

lab_app = typer.Typer(help="harness-lab レコードを操作します。")


@lab_app.command("import-feedback")
def import_feedback_alias(path: str) -> None:
    """`hops feedback import` のエイリアスです。"""
    import_feedback(path=Path(path))


@lab_app.command("import")
def import_alias(path: str) -> None:
    """サニタイズ済みフィードバックバンドルをインポートする短いエイリアスです。"""
    import_feedback(path=Path(path))


@lab_app.command("new-eval-case")
def new_eval_case(from_id: str = typer.Option(..., "--from"), template: str | None = typer.Option(None, "--template")) -> None:
    """インポート済みフィードバックを評価ケースに変換します。"""
    del template
    root = find_root()
    project = load_project(root)
    feedback_path = find_record(project, from_id)
    frontmatter, _ = read_record(feedback_path)
    classification = frontmatter.get("classification", {})
    path = create_eval_case(
        project,
        feedback_id=str(frontmatter.get("id", from_id)),
        title=f"{feedback_path.stem} を評価",
        capability=str(classification.get("capability", "unclassified")),
        failure_class=str(classification.get("failure_class", "unclassified")),
    )
    refresh_views(root, project.overlay_path)
    typer.echo(path.relative_to(root).as_posix())


def register(app: typer.Typer) -> None:
    app.add_typer(lab_app, name="lab")
