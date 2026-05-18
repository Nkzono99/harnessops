from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import typer

from harnessops.core.agent_plugin import install_global_plugin


def _codex_cli_status() -> dict[str, Any]:
    path = shutil.which("codex")
    if not path:
        return {
            "found": False,
            "path": None,
            "version": None,
            "install_hint": "npm install -g @openai/codex@latest",
            "docs": "https://github.com/openai/codex",
        }
    version = None
    try:
        completed = subprocess.run(
            [path, "--version"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        version = (completed.stdout or completed.stderr).strip() or None
    except (OSError, subprocess.SubprocessError):
        version = None
    return {
        "found": True,
        "path": path,
        "version": version,
        "install_hint": None,
        "docs": "https://github.com/openai/codex",
    }


def _activation_steps() -> list[str]:
    return [
        "Open a new Codex session in the target repository.",
        "Run `/plugin`.",
        "Enable `HarnessOps Global` / `harnessops-global`.",
        "Ask Codex to use HarnessOps local state, for example: `このrepoを HarnessOps local state で使えるようにして。repoにはファイルを作らないで。`",
    ]


def install_codex_plugin_command(
    force: bool = typer.Option(False, "--force"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    destination: Path | None = typer.Option(None, "--destination"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """HarnessOps Global Codex plugin をユーザー領域へインストールします。"""
    result = install_global_plugin(
        host="codex",
        destination=destination,
        force=force,
        dry_run=dry_run,
    )
    payload = {
        "plugin": result,
        "codex_cli": _codex_cli_status(),
        "activation_steps": _activation_steps(),
    }
    if json_output:
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return

    prefix = "[dry-run] " if dry_run else ""
    typer.echo(f"{prefix}installed HarnessOps Global Codex plugin")
    typer.echo(f"destination: {result['destination']}")
    typer.echo(f"manifest: {result['manifest']}")
    typer.echo(f"files: updated={len(result['updated'])} unchanged={len(result['unchanged'])} written_new={len(result['written_new'])}")
    if result["written_new"]:
        typer.echo("conflict copies:")
        for item in result["written_new"]:
            typer.echo(f"- {item['new']}")

    status = payload["codex_cli"]
    if status["found"]:
        version = f" ({status['version']})" if status["version"] else ""
        typer.echo(f"codex CLI: found {status['path']}{version}")
    else:
        typer.echo("codex CLI: not found on PATH")
        typer.echo("install Codex CLI, then open a new terminal:")
        typer.echo(f"- {status['install_hint']}")
        typer.echo(f"- docs: {status['docs']}")

    typer.echo("enable in Codex:")
    for index, step in enumerate(payload["activation_steps"], start=1):
        typer.echo(f"{index}. {step}")


def register(app: typer.Typer) -> None:
    app.command("install-codex-plugin")(install_codex_plugin_command)
