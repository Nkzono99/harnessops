from __future__ import annotations

import json
from pathlib import Path

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.registry import (
    hops_home,
    import_local_pack,
    merge_local_state,
    pack_local_project,
)
from harnessops.core.render import refresh_project_views

local_app = typer.Typer(help="storage=local project state の pack/import/merge を扱います。")


@local_app.command("pack")
def pack(
    output: Path | None = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """現在の storage=local project state を zip にまとめます。"""
    project = load_project(find_root())
    pack_output = output
    if pack_output is None:
        pack_id = project.registry_id or project.root.name
        pack_output = hops_home() / "exports" / f"{pack_id}-local-state.zip"
    elif not pack_output.is_absolute():
        pack_output = Path.cwd() / pack_output
    out_path = pack_local_project(project, pack_output)
    payload = {"path": out_path.as_posix()}
    if json_output:
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return
    typer.echo(out_path.as_posix())


@local_app.command("import")
def import_pack(
    path: Path,
    force: bool = typer.Option(False, "--force"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """local state pack を global registry へ取り込みます。"""
    try:
        result = import_local_pack(path if path.is_absolute() else Path.cwd() / path, force=force)
    except (FileExistsError, FileNotFoundError, KeyError, ValueError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    payload = {key: value.as_posix() if isinstance(value, Path) else value for key, value in result.items()}
    if json_output:
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return
    typer.echo(f"imported: {payload['id']}")
    typer.echo(f"state: {payload['state_root']}")


@local_app.command("merge")
def merge(
    source: Path,
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """pack または state directory から現在の storage=local project へ records を merge します。"""
    project = load_project(find_root())
    try:
        result = merge_local_state(project, source if source.is_absolute() else Path.cwd() / source)
    except (FileNotFoundError, ValueError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    refresh_project_views(project)
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return
    typer.echo(f"copied: {len(result['copied'])}")
    typer.echo(f"skipped: {len(result['skipped'])}")
    typer.echo(f"conflicted: {len(result['conflicted'])}")


def register(app: typer.Typer) -> None:
    app.add_typer(local_app, name="local")
