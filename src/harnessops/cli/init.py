from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from harnessops.core.overlay import UnsafeOverwrite, init_overlay
from harnessops.core.detect import detect_repository
from harnessops.core.project import load_project
from harnessops.core.validation import doctor as doctor_project
from harnessops.profiles.registry import load_profile


def _run_init(
    *,
    profile: Optional[str],
    mode: Optional[str],
    path: Optional[str],
    with_agent_bridge: bool,
    dry_run: bool,
    force: bool,
) -> None:
    root = Path.cwd().resolve()
    if profile is None:
        detected = detect_repository(root)
        profile = detected.get("profile")
        if not profile:
            typer.echo("profile not provided and detection did not find a recommended profile")
            raise typer.Exit(3)
    profile_data = load_profile(profile)
    try:
        result = init_overlay(
            root,
            profile_data,
            mode=mode,
            overlay_path=path,
            with_agent_bridge=with_agent_bridge,
            dry_run=dry_run,
            force=force,
        )
    except UnsafeOverwrite as exc:
        typer.echo(str(exc))
        raise typer.Exit(2) from exc
    typer.echo(json.dumps(result, indent=2, sort_keys=True))
    if not dry_run:
        project = load_project(root)
        report = doctor_project(project, check_records=True)
        if not report["ok"]:
            typer.echo(json.dumps(report, indent=2, sort_keys=True))
            raise typer.Exit(1)


def init_command(
    profile: Optional[str] = typer.Option(None, "--profile"),
    mode: Optional[str] = typer.Option(None, "--mode"),
    path: Optional[str] = typer.Option(None, "--path"),
    with_agent_bridge: bool = typer.Option(False, "--with-agent-bridge"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    force: bool = typer.Option(False, "--force"),
) -> None:
    """Create HarnessOps metadata and overlay for a repository."""
    _run_init(profile=profile, mode=mode, path=path, with_agent_bridge=with_agent_bridge, dry_run=dry_run, force=force)


def link_command(
    profile: Optional[str] = typer.Option(None, "--profile"),
    mode: Optional[str] = typer.Option(None, "--mode"),
    path: Optional[str] = typer.Option(None, "--path"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    force: bool = typer.Option(False, "--force"),
) -> None:
    """Link an existing repository to HarnessOps."""
    _run_init(profile=profile, mode=mode, path=path, with_agent_bridge=False, dry_run=dry_run, force=force)


def register(app: typer.Typer) -> None:
    app.command("init")(init_command)
    app.command("link")(link_command)
