from __future__ import annotations

import json

import typer

from harnessops.core.agent_bridge import write_bridge
from harnessops.core.paths import find_root

agent_app = typer.Typer(help="Install or verify agent bridge/plugin artifacts.")


@agent_app.command("bridge")
def bridge(codex: bool = typer.Option(False, "--codex"), claude: bool = typer.Option(False, "--claude"), force: bool = typer.Option(False, "--force")) -> None:
    """Generate a thin repo-local bridge skill."""
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
    """Install a repo-local bridge; full plugins ship with HarnessOps."""
    if scope != "repo":
        typer.echo("MVP supports repo scope only")
        raise typer.Exit(1)
    bridge(codex=codex, claude=claude, force=force)


@agent_app.command("verify")
def verify() -> None:
    """Verify repo-local bridge or packaged plugin artifacts."""
    root = find_root()
    expected = root / ".agents" / "skills" / "harnessops-bridge" / "SKILL.md"
    packaged = root / "plugins" / "codex" / "harnessops" / ".codex-plugin" / "plugin.json"
    if expected.exists() or packaged.exists():
        typer.echo("ok")
    else:
        typer.echo("no bridge or packaged plugin found")
        raise typer.Exit(1)


def register(app: typer.Typer) -> None:
    app.add_typer(agent_app, name="agent")

