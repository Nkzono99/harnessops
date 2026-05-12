from __future__ import annotations

from pathlib import Path

import typer

from harnessops.cli.feedback import import_feedback
from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.records import create_eval_case, create_lab_feedback, find_record, read_record
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


@lab_app.command("capture")
def capture(
    title: str = typer.Option(..., "--title"),
    summary: str = typer.Option(..., "--summary"),
    expected_change: str = typer.Option(..., "--expected-change"),
    reproduction: str = typer.Option("ローカル改善作業中に観測。", "--reproduction"),
    capability: str = typer.Option("harness_lab_traceability", "--capability"),
    failure_class: str = typer.Option("missing_lab_capture", "--failure-class"),
    source_ref: str | None = typer.Option(None, "--source-ref"),
) -> None:
    """ローカル改善やissue前の観測を harness-lab feedback として記録します。"""
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        typer.echo("lab capture には upstream-lab または meta-lab mode が必要です")
        raise typer.Exit(1)
    path = create_lab_feedback(
        project,
        title=title,
        summary=summary,
        reproduction=reproduction,
        expected_change=expected_change,
        capability=capability,
        failure_class=failure_class,
        source_ref=source_ref,
    )
    refresh_views(root, project.overlay_path)
    typer.echo(path.relative_to(root).as_posix())


@lab_app.command("refresh-views")
def refresh_lab_views() -> None:
    """harness-lab の生成ビューを再生成します。"""
    root = find_root()
    project = load_project(root)
    written = refresh_views(root, project.overlay_path)
    typer.echo("\n".join(path.relative_to(root).as_posix() for path in written))


def register(app: typer.Typer) -> None:
    app.add_typer(lab_app, name="lab")
