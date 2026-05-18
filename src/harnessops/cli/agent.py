from __future__ import annotations

import json

import typer

from harnessops.core.agent_asset_sync import sync_packaged_skill_assets
from harnessops.core.agent_bridge import refresh_bridge_files
from harnessops.cli.codex_plugin import install_codex_plugin_command
from harnessops.core.paths import find_root

agent_app = typer.Typer(help="repo-local エージェントブリッジ/skill を生成または検証します。")


@agent_app.command("bridge")
def bridge(codex: bool = typer.Option(False, "--codex"), claude: bool = typer.Option(False, "--claude"), no_github_flow: bool = typer.Option(False, "--no-github-flow"), force: bool = typer.Option(False, "--force")) -> None:
    """リポジトリローカルの HarnessOps skills を生成します。"""
    if not codex and not claude:
        codex = True
    root = find_root()
    result = refresh_bridge_files(
        root,
        codex=codex,
        claude=claude,
        force=force,
        update_lock=(root / ".harnessops" / "lock.json").exists(),
        github_flow=False if no_github_flow else None,
    )
    typer.echo(json.dumps(result["checked"], indent=2))


@agent_app.command("install")
def install(
    codex: bool = typer.Option(False, "--codex"),
    claude: bool = typer.Option(False, "--claude"),
    no_github_flow: bool = typer.Option(False, "--no-github-flow"),
    scope: str = typer.Option("repo", "--scope"),
    force: bool = typer.Option(False, "--force"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    destination: str | None = typer.Option(None, "--destination"),
) -> None:
    """repo-local skill または user global plugin を生成します。"""
    if not codex and not claude:
        codex = True
    if scope == "repo":
        bridge(codex=codex, claude=claude, no_github_flow=no_github_flow, force=force)
        return
    if scope in {"user", "global"} and codex and not claude:
        from pathlib import Path

        install_codex_plugin_command(
            destination=Path(destination) if destination else None,
            force=force,
            dry_run=dry_run,
            json_output=True,
        )
        return
    if scope in {"user", "global"} and claude:
        typer.echo("global plugin install は現在 Codex のみ対応です")
        raise typer.Exit(1)
    typer.echo("scope は repo、user、global のいずれかを指定してください")
    raise typer.Exit(1)


@agent_app.command("verify")
def verify() -> None:
    """repo-local skillまたは同梱プラグイン成果物を検証します。"""
    root = find_root()
    expected = root / ".agents" / "skills" / "harnessops-bridge" / "SKILL.md"
    if expected.exists():
        typer.echo("ok")
    else:
        typer.echo("repo-local エージェントブリッジが見つかりません")
        raise typer.Exit(1)


@agent_app.command("sync-packaged-skills")
def sync_packaged_skills(
    codex: bool = typer.Option(False, "--codex"),
    claude: bool = typer.Option(False, "--claude"),
    check: bool = typer.Option(False, "--check", help="差分を検出するだけで書き込みません。"),
    json_output: bool = typer.Option(False, "--json", help="機械可読JSONで出力します。"),
) -> None:
    """repo-local hops skills を packaged agent assets へ同期します。"""
    if not codex and not claude:
        codex = True
        claude = True
    hosts = tuple(host for enabled, host in ((codex, "codex"), (claude, "claude")) if enabled)
    root = find_root()
    try:
        result = sync_packaged_skill_assets(root, hosts=hosts, check=check)
    except (FileNotFoundError, ValueError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    if json_output:
        typer.echo(json.dumps(result, indent=2, sort_keys=True))
    else:
        typer.echo(f"checked: {len(result['checked'])}")
        typer.echo(f"updated: {len(result['updated'])}")
        typer.echo(f"unchanged: {len(result['unchanged'])}")
        if result["missing"]:
            typer.echo(f"missing: {len(result['missing'])}")
        if result["drifted"]:
            typer.echo(f"drifted: {len(result['drifted'])}")
        if result["retired"]:
            typer.echo(f"retired: {len(result['retired'])}")
    if not result["ok"]:
        raise typer.Exit(1)


def register(app: typer.Typer) -> None:
    app.add_typer(agent_app, name="agent")
