from __future__ import annotations

import json

import typer

from harnessops.core.agent_bridge import write_bridge
from harnessops.core.migration import apply_migrations as apply_pending_migrations, check_migrations
from harnessops.core.overlay import refresh_managed_files
from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.validation import doctor as doctor_project


def update_harness_command(
    apply_migrations: bool = typer.Option(False, "--apply-migrations"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    force: bool = typer.Option(False, "--force"),
    agent_bridge: bool = typer.Option(False, "--agent-bridge"),
    codex: bool = typer.Option(False, "--codex"),
    claude: bool = typer.Option(False, "--claude"),
    force_agent_bridge: bool = typer.Option(
        False,
        "--force-agent-bridge/--no-force-agent-bridge",
    ),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """HarnessOps 管理状態を現在の hops 実装に合わせて更新または検証します。"""
    root = find_root()
    project = load_project(root)

    if apply_migrations and not dry_run:
        migration_entry = apply_pending_migrations(project)
        migration = check_migrations(project)
    else:
        migration_entry = None
        migration = check_migrations(project)

    managed = refresh_managed_files(
        root,
        project.overlay_mode,
        project.overlay_path,
        force=force,
        dry_run=dry_run,
    )

    existing_codex = (
        root / ".agents" / "skills" / "harnessops-bridge" / "SKILL.md"
    ).exists()
    existing_claude = (
        root / ".claude" / "skills" / "harnessops-bridge" / "SKILL.md"
    ).exists()
    refresh_codex = codex or existing_codex or (agent_bridge and not claude)
    refresh_claude = claude or existing_claude

    agent_paths: list[str] = []
    if refresh_codex or refresh_claude:
        if dry_run:
            agent_paths = ["<dry-run>"]
        else:
            agent_paths = [
                path.relative_to(root).as_posix()
                for path in write_bridge(
                    root,
                    codex=refresh_codex,
                    claude=refresh_claude,
                    force=force_agent_bridge,
                )
            ]

    report = doctor_project(project, check_records=True)
    if not migration["ok"]:
        report["ok"] = False
        report["errors"].extend(f"未適用マイグレーション: {item}" for item in migration["pending"])

    result = {
        "ok": report["ok"],
        "migration": {
            "applied": str(migration_entry.relative_to(root)) if migration_entry else None,
            "pending": migration["pending"],
        },
        "managed_files": managed,
        "agent_bridge": {
            "refreshed": bool(agent_paths),
            "paths": agent_paths,
        },
        "doctor": report,
    }
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        prefix = "[dry-run] " if dry_run else ""
        typer.echo(f"{prefix}{'ok' if result['ok'] else '失敗'}")
        if migration_entry:
            typer.echo(f"migration: applied {migration_entry.relative_to(root).as_posix()}")
        elif migration["pending"]:
            typer.echo("migration: pending")
        else:
            typer.echo(f"{prefix}migration: up-to-date")
        if managed["updated"]:
            typer.echo(f"{prefix}managed files: updated {len(managed['updated'])}")
        if managed["written_new"]:
            typer.echo(f"{prefix}managed files: wrote {len(managed['written_new'])} .new file(s)")
            for item in managed["written_new"]:
                typer.echo(f"  {item['new']}")
        if agent_paths:
            typer.echo(f"{prefix}agent bridge: checked {len(agent_paths)} paths")
        else:
            typer.echo(f"{prefix}agent bridge: unchanged")
        for warning in report["warnings"]:
            typer.echo(f"警告: {warning}")
        for error in report["errors"]:
            typer.echo(f"エラー: {error}")
    if not result["ok"]:
        raise typer.Exit(1)


def register(app: typer.Typer) -> None:
    app.command("update-harness")(update_harness_command)
