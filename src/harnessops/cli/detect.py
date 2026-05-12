from __future__ import annotations

import json
from pathlib import Path

import typer

from harnessops.core.detect import detect_repository


def detect(json_output: bool = typer.Option(False, "--json")) -> None:
    """リポジトリ種別と推奨プロファイルを推定します。"""
    root = Path.cwd().resolve()
    result = detect_repository(root)
    result["root"] = str(root)
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))
        return
    typer.echo(f"ルート: {root}")
    typer.echo(f"プロファイル: {result.get('profile')}")
    typer.echo(f"リポジトリ種別: {result.get('repository_kind')}")
    typer.echo(f"検出元: {result.get('source')}")
    if result.get("markers"):
        typer.echo("マーカー: " + ", ".join(result["markers"]))


def register(app: typer.Typer) -> None:
    app.command("detect")(detect)
