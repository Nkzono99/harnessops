from __future__ import annotations

import json
from pathlib import Path

import typer

from harnessops.core.detect import detect_repository


def detect(json_output: bool = typer.Option(False, "--json")) -> None:
    """Infer repository type and recommended profile."""
    root = Path.cwd().resolve()
    result = detect_repository(root)
    result["root"] = str(root)
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))
        return
    typer.echo(f"root: {root}")
    typer.echo(f"profile: {result.get('profile')}")
    typer.echo(f"repository_kind: {result.get('repository_kind')}")
    typer.echo(f"source: {result.get('source')}")
    if result.get("markers"):
        typer.echo("markers: " + ", ".join(result["markers"]))


def register(app: typer.Typer) -> None:
    app.command("detect")(detect)
