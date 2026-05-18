from __future__ import annotations

from typing import Optional

import typer

from harnessops.cli.deprecation import warn_if_deprecated
from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.lab_records import create_failure, create_feedback_from_failure
from harnessops.core.record_index import find_record
from harnessops.core.record_io import read_record
from harnessops.core.render import refresh_project_views
from harnessops.core.routing import classify_text
from harnessops.core.routing import DISPOSITIONS


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
    """プロジェクト側の失敗レコードを作成します。"""
    warn_if_deprecated("add-failure", "hops feedback add-failure")
    del interactive
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"feedback-source", "local-and-feedback"}:
        typer.echo("add-failure には feedback-source または local-and-feedback mode が必要です")
        raise typer.Exit(1)
    file_text = ""
    if from_file:
        file_text = (root / from_file).read_text(encoding="utf-8")
    routing = classify_text(" ".join([title, context, what_happened, file_text]), target=target)
    if disposition is not None and disposition not in DISPOSITIONS:
        typer.echo(f"disposition が不正です: {disposition}")
        raise typer.Exit(1)
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
    refresh_project_views(project)
    typer.echo(project.display_path(path))


def add_feedback_command(
    from_id: str = typer.Option(..., "--from"),
    target: Optional[str] = typer.Option(None, "--target"),
    feedback_type: Optional[str] = typer.Option(None, "--type"),
    title: Optional[str] = typer.Option(None, "--title"),
    summary: str = typer.Option("", "--summary"),
) -> None:
    """既存の失敗からフィードバック下書きを作成します。

    下書きは `hops feedback export --sanitize` でエクスポートされるまで非公開です。
    """
    warn_if_deprecated("add-feedback", "hops feedback add")
    root = find_root()
    project = load_project(root)
    failure_frontmatter, _ = read_record(find_record(project, from_id))
    resolved_target = target or failure_frontmatter.get("disposition", {}).get("target") or "harnessops"
    path = create_feedback_from_failure(
        project,
        failure_ref=from_id,
        target=resolved_target,
        feedback_type=feedback_type,
        title=title,
        summary=summary,
    )
    refresh_project_views(project)
    typer.echo(project.display_path(path))


def register(app: typer.Typer) -> None:
    app.command("add-failure", hidden=True)(add_failure_command)
    app.command("add-feedback", hidden=True)(add_feedback_command)
