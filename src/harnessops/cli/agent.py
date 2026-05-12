from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import typer

from harnessops.core.agent_bridge import packaged_plugin_source, refresh_bridge_files
from harnessops.core.paths import find_root

agent_app = typer.Typer(help="エージェントブリッジ/プラグイン成果物をインストールまたは検証します。")
PLUGIN_NAME = "harnessops"


def _copy_plugin(source: Path, destination: Path, *, force: bool) -> None:
    if not source.exists():
        typer.echo(f"同梱プラグインソースが見つかりません: {source}")
        raise typer.Exit(1)
    if destination.exists():
        if not force:
            typer.echo(f"プラグインは既に存在します: {destination}")
            raise typer.Exit(2)
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)


def _write_codex_user_marketplace(home: Path) -> Path:
    marketplace = home / ".agents" / "plugins" / "marketplace.json"
    plugin_path = "./.codex/plugins/harnessops"
    entry = {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": plugin_path,
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Productivity",
    }
    if marketplace.exists():
        data = json.loads(marketplace.read_text(encoding="utf-8"))
    else:
        data = {
            "name": "local",
            "interface": {
                "displayName": "Local Plugins",
            },
            "plugins": [],
        }
    plugins = data.setdefault("plugins", [])
    for index, plugin in enumerate(plugins):
        if plugin.get("name") == PLUGIN_NAME:
            plugins[index] = entry
            break
    else:
        plugins.append(entry)
    marketplace.parent.mkdir(parents=True, exist_ok=True)
    marketplace.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return marketplace


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
    """repo-local skillを生成するか、任意の同梱プラグインをユーザー領域へコピーします。"""
    if not codex and not claude:
        codex = True
    if scope == "repo":
        bridge(codex=codex, claude=claude, force=force)
        return
    if scope != "user":
        typer.echo("scope は repo または user で指定してください")
        raise typer.Exit(1)
    home = Path(os.environ.get("HOME") or Path.home())
    installed: list[dict[str, str]] = []
    for enabled, host, plugin_dir in [
        (codex, "codex", home / ".codex" / "plugins" / PLUGIN_NAME),
        (claude, "claude", home / ".claude" / "plugins" / PLUGIN_NAME),
    ]:
        if not enabled:
            continue
        source = packaged_plugin_source(host)
        _copy_plugin(source, plugin_dir, force=force)
        result = {
            "host": host,
            "plugin": plugin_dir.as_posix(),
        }
        if host == "codex":
            marketplace = _write_codex_user_marketplace(home)
            result["marketplace"] = marketplace.as_posix()
            result["activate"] = f"codex plugin marketplace add {home.as_posix()}"
        installed.append(result)
    typer.echo(json.dumps(installed, indent=2))


@agent_app.command("verify")
def verify() -> None:
    """repo-local skillまたは同梱プラグイン成果物を検証します。"""
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
