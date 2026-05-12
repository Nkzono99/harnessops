from __future__ import annotations

import json
from typing import Any

import typer

from harnessops.core.migration import apply_migrations, check_migrations
from harnessops.core.paths import find_root
from harnessops.core.project import load_project


def migrate_command(
    check: bool = typer.Option(False, "--check"),
    apply: bool = typer.Option(False, "--apply"),  # noqa: A002
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """HarnessOps レイアウトマイグレーションを確認または適用します。"""
    project = load_project(find_root())
    result: dict[str, Any]
    if apply:
        entry = apply_migrations(project)
        result = {"ok": True, "pending": [], "entry": str(entry) if entry else None}
    else:
        del check
        result = check_migrations(project)
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))
    else:
        typer.echo("未適用マイグレーションはありません" if result["ok"] else "未適用マイグレーションがあります")
        pending = result.get("pending", [])
        for item in pending if isinstance(pending, list) else []:
            typer.echo(item)
    if not result["ok"]:
        raise typer.Exit(1)


def register(app: typer.Typer) -> None:
    app.command("migrate")(migrate_command)
