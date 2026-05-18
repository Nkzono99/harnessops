from __future__ import annotations

import json

import typer

from harnessops.core.detect import detect_repository
from harnessops.core.paths import find_root
from harnessops.core.project import load_project, project_file
from harnessops.core.registry import (
    link_local_project,
    project_payload,
    read_registry,
    unlink_local_project,
)

project_app = typer.Typer(help="global registry で HarnessOps project を解決・リンクします。")


@project_app.command("link")
def link(
    profile: str | None = typer.Option(None, "--profile"),
    mode: str | None = typer.Option(None, "--mode"),
    storage: str = typer.Option("local", "--storage"),
    project_id: str | None = typer.Option(None, "--id"),
    force: bool = typer.Option(False, "--force"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """repo を汚さず global registry + local state にリンクします。"""
    root = find_root()
    if storage != "local":
        typer.echo("project link は --storage local 専用です。repo-local 利用は `hops init` または `hops link` を使ってください。")
        raise typer.Exit(1)
    if project_file(root).exists():
        typer.echo("repo-local .harnessops/project.toml があるため global registry link は作成しません。repo-local 利用を続けるか、別の作業ツリーで storage=local を使ってください。")
        raise typer.Exit(1)
    resolved_profile = profile
    if resolved_profile is None:
        detected = detect_repository(root)
        resolved_profile = detected.get("profile")
        if not resolved_profile:
            typer.echo("profile が指定されておらず、検出でも推奨プロファイルが見つかりません")
            raise typer.Exit(3)
    project = link_local_project(
        root,
        profile_id=resolved_profile,
        mode=mode,
        project_id=project_id,
        force=force,
    )
    payload = project_payload(project)
    if json_output:
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return
    typer.echo(f"linked: {payload['id']}")
    typer.echo(f"root: {payload['root']}")
    typer.echo(f"state: {payload['state_root']}")
    typer.echo(f"overlay: {payload['overlay_dir']}")


@project_app.command("resolve")
def resolve(json_output: bool = typer.Option(False, "--json")) -> None:
    """現在の cwd から repo-local または global registry の project を解決します。"""
    root = find_root()
    try:
        project = load_project(root)
    except FileNotFoundError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    payload = project_payload(project)
    if json_output:
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return
    typer.echo(f"id: {payload['id'] or 'repo-local'}")
    typer.echo(f"root: {payload['root']}")
    typer.echo(f"profile: {payload['profile']}")
    typer.echo(f"mode: {payload['mode']}")
    typer.echo(f"storage: {payload['storage']}")
    typer.echo(f"overlay: {payload['overlay_dir']}")


@project_app.command("list")
def list_projects(json_output: bool = typer.Option(False, "--json")) -> None:
    """global registry に登録された local projects を表示します。"""
    registry = read_registry()
    projects = registry.get("projects", []) or []
    if json_output:
        typer.echo(json.dumps(projects, ensure_ascii=False, indent=2, sort_keys=True))
        return
    if not projects:
        typer.echo("登録済み project はありません")
        return
    for item in projects:
        typer.echo(f"- {item.get('id')} {item.get('root')} [{item.get('mode')}]")


@project_app.command("unlink")
def unlink(
    delete_state: bool = typer.Option(False, "--delete-state"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """現在の cwd の global registry link を削除します。"""
    result = unlink_local_project(find_root(), delete_state=delete_state)
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, default=str))
        return
    typer.echo("removed" if result["removed"] else "not linked")


def register(app: typer.Typer) -> None:
    app.add_typer(project_app, name="project")
