from __future__ import annotations

import json

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.validation import doctor as doctor_project
from harnessops.core.migration import check_migrations


def doctor_command(
    json_output: bool = typer.Option(False, "--json"),
    provider: bool = typer.Option(False, "--provider"),
    check_overlay: bool = typer.Option(False, "--check-overlay"),
    check_records: bool = typer.Option(False, "--check-records"),
    allow_pending: bool = typer.Option(False, "--allow-pending"),
) -> None:
    """HarnessOps リンク、オーバーレイ、プロファイル、レコードを検証します。"""
    del check_overlay
    project = load_project(find_root())
    result = doctor_project(project, check_records=check_records)
    migration = check_migrations(project)
    if not migration["ok"] and not allow_pending:
        result["ok"] = False
        result["errors"].extend(f"未適用マイグレーション: {item}" for item in migration["pending"])
    if provider:
        result["provider"] = {"checked": False, "message": "MVP doctor ではプロバイダコマンド実行は有効化されていません"}
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))
    else:
        typer.echo("ok" if result["ok"] else "失敗")
        for warning in result["warnings"]:
            typer.echo(f"警告: {warning}")
        for error in result["errors"]:
            typer.echo(f"エラー: {error}")
    if not result["ok"]:
        raise typer.Exit(1)


def register(app: typer.Typer) -> None:
    app.command("doctor")(doctor_command)
