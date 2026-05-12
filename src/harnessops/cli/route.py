from __future__ import annotations

import json
from typing import Optional

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.records import dump_record, find_record, read_record
from harnessops.core.render import refresh_views
from harnessops.core.routing import classify_text


def route_command(
    record: Optional[str] = typer.Option(None, "--record"),
    text: str = typer.Option("", "--text"),
    target: Optional[str] = typer.Option(None, "--target"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Classify a record into a HarnessOps disposition."""
    root = find_root()
    project = load_project(root)
    body = text
    record_path = None
    frontmatter = {}
    if record:
        record_path = find_record(project, record)
        frontmatter, body = read_record(record_path)
    disposition = classify_text(" ".join([body, text]), target=target or frontmatter.get("disposition", {}).get("target"))
    if record_path:
        frontmatter["disposition"] = disposition
        record_path.write_text(dump_record(frontmatter, body), encoding="utf-8")
        refresh_views(root, project.overlay_path)
    if json_output:
        typer.echo(json.dumps(disposition, indent=2, sort_keys=True))
    else:
        typer.echo(disposition["type"])


def register(app: typer.Typer) -> None:
    app.command("route")(route_command)

