from __future__ import annotations

import json

import typer

from harnessops.core.agent_bridge import refresh_bridge_files
from harnessops.core.paths import find_root

agent_app = typer.Typer(help="repo-local エージェントブリッジ/skill を生成または検証します。")


@agent_app.command("bridge")
def bridge(codex: bool = typer.Option(False, "--codex"), claude: bool = typer.Option(False, "--claude"), force: bool = typer.Option(False, "--force")) -> None:
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
    )
    typer.echo(json.dumps(result["checked"], indent=2))


@agent_app.command("install")
def install(
    codex: bool = typer.Option(False, "--codex"),
    claude: bool = typer.Option(False, "--claude"),
    scope: str = typer.Option("repo", "--scope"),
    force: bool = typer.Option(False, "--force"),
) -> None:
    """repo-local skillを生成します。"""
    if not codex and not claude:
        codex = True
    if scope == "repo":
        bridge(codex=codex, claude=claude, force=force)
        return
    typer.echo("user plugin install は廃止されました。repo-local skill は --scope repo または `hops agent bridge` で生成してください。")
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


def register(app: typer.Typer) -> None:
    app.add_typer(agent_app, name="agent")
