from __future__ import annotations

import json
import shutil
from pathlib import Path

import typer

from harnessops.core.agent_bridge import write_bridge
from harnessops.core.paths import find_root

agent_app = typer.Typer(help="エージェントブリッジ/プラグイン成果物をインストールまたは検証します。")


@agent_app.command("bridge")
def bridge(codex: bool = typer.Option(False, "--codex"), claude: bool = typer.Option(False, "--claude"), force: bool = typer.Option(False, "--force")) -> None:
    """薄いリポジトリローカルブリッジスキルを生成します。"""
    if not codex and not claude:
        codex = True
    root = find_root()
    paths = write_bridge(root, codex=codex, claude=claude, force=force)
    typer.echo(json.dumps([path.relative_to(root).as_posix() for path in paths], indent=2))


@agent_app.command("install")
def install(
    codex: bool = typer.Option(False, "--codex"),
    claude: bool = typer.Option(False, "--claude"),
    scope: str = typer.Option("repo", "--scope"),
    force: bool = typer.Option(False, "--force"),
) -> None:
    """リポジトリローカルブリッジをインストールするか、同梱プラグインをユーザープラグインディレクトリへコピーします。"""
    if not codex and not claude:
        codex = True
    root = find_root()
    if scope == "repo":
        bridge(codex=codex, claude=claude, force=force)
        return
    if scope != "user":
        typer.echo("scope は repo または user で指定してください")
        raise typer.Exit(1)
    home = Path.home()
    installed = []
    for enabled, host, plugin_dir in [
        (codex, "codex", home / ".codex" / "plugins" / "harnessops"),
        (claude, "claude", home / ".claude" / "plugins" / "harnessops"),
    ]:
        if not enabled:
            continue
        source = root / "plugins" / host / "harnessops"
        if not source.exists():
            source = Path(__file__).resolve().parents[3] / "plugins" / host / "harnessops"
        if not source.exists():
            typer.echo(f"同梱 {host} プラグインソースが見つかりません")
            raise typer.Exit(1)
        if plugin_dir.exists():
            if not force:
                typer.echo(f"プラグインは既に存在します: {plugin_dir}")
                raise typer.Exit(2)
            shutil.rmtree(plugin_dir)
        plugin_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, plugin_dir)
        installed.append(plugin_dir.as_posix())
    typer.echo(json.dumps(installed, indent=2))


@agent_app.command("verify")
def verify() -> None:
    """リポジトリローカルブリッジまたは同梱プラグイン成果物を検証します。"""
    root = find_root()
    expected = root / ".agents" / "skills" / "harnessops-bridge" / "SKILL.md"
    packaged = root / "plugins" / "codex" / "harnessops" / ".codex-plugin" / "plugin.json"
    if expected.exists() or packaged.exists():
        typer.echo("ok")
    else:
        typer.echo("ブリッジまたは同梱プラグインが見つかりません")
        raise typer.Exit(1)


def register(app: typer.Typer) -> None:
    app.add_typer(agent_app, name="agent")
