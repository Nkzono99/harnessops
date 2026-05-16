from __future__ import annotations

import json
from typing import Any

import typer

from harnessops import __version__
from harnessops.core.agent_bridge import refresh_bridge_files
from harnessops.core.gitignore import ensure_gitignore
from harnessops.core.migration import apply_migrations as apply_pending_migrations, check_migrations
from harnessops.core.overlay import refresh_managed_files
from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.render import refresh_views
from harnessops.core.upgrade_chain import (
    GRANULARITIES,
    UpgradePlan,
    UpgradeRun,
    build_upgrade_plan,
    run_upgrade_chain,
    upgrade_chain_active,
)
from harnessops.core.validation import doctor as doctor_project


def _chain_passthrough_args(
    *,
    apply_migrations: bool,
    force: bool,
    agent_bridge: bool,
    codex: bool,
    claude: bool,
    force_agent_bridge: bool,
) -> list[str]:
    args: list[str] = []
    if apply_migrations:
        args.append("--apply-migrations")
    if force:
        args.append("--force")
    if agent_bridge:
        args.append("--agent-bridge")
    if codex:
        args.append("--codex")
    if claude:
        args.append("--claude")
    if force_agent_bridge:
        args.append("--force-agent-bridge")
    return args


def _echo_upgrade_plan(plan: UpgradePlan, *, prefix: str = "") -> None:
    latest = plan.latest_pypi_version or "unknown"
    recorded = plan.recorded_version or "unknown"
    typer.echo(f"{prefix}upgrade chain: {'needed' if plan.needed else 'not needed'}")
    typer.echo(f"{prefix}  repo managed artifacts: {recorded}")
    typer.echo(f"{prefix}  current hops runtime:   {plan.current_version}")
    typer.echo(f"{prefix}  target version:         {plan.target_version}")
    typer.echo(f"{prefix}  latest PyPI release:    {latest}")
    typer.echo(f"{prefix}  granularity:            {plan.granularity}")
    if plan.reason:
        typer.echo(f"{prefix}  reason:                 {plan.reason}")
    for index, step in enumerate(plan.steps, start=1):
        typer.echo(f"{prefix}  {index}. {step.version}")
        typer.echo(f"{prefix}     {' '.join(step.command)}")


def _echo_upgrade_runs(runs: list[UpgradeRun], *, prefix: str = "") -> None:
    for run in runs:
        status = "ok" if run.returncode == 0 else f"failed ({run.returncode})"
        typer.echo(f"{prefix}upgrade chain: {run.version} {status}")
        if run.stdout.strip():
            typer.echo(run.stdout.rstrip())
        if run.stderr.strip():
            typer.echo(run.stderr.rstrip(), err=True)


def update_harness_command(
    apply_migrations: bool = typer.Option(False, "--apply-migrations"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    force: bool = typer.Option(False, "--force"),
    agent_bridge: bool = typer.Option(False, "--agent-bridge"),
    codex: bool = typer.Option(False, "--codex"),
    claude: bool = typer.Option(False, "--claude"),
    no_github_flow: bool = typer.Option(False, "--no-github-flow"),
    force_agent_bridge: bool = typer.Option(
        False,
        "--force-agent-bridge/--no-force-agent-bridge",
    ),
    plan_upgrade: bool = typer.Option(False, "--plan-upgrade"),
    apply_upgrade_chain: bool = typer.Option(False, "--apply-upgrade-chain"),
    upgrade_chain: bool = typer.Option(
        True,
        "--upgrade-chain/--no-upgrade-chain",
        help="古い HarnessOps managed artifacts を checkpoint 版で段階更新します。",
    ),
    upgrade_granularity: str = typer.Option(
        "minor",
        "--upgrade-granularity",
        help="upgrade chain の checkpoint 粒度: patch, minor, major。",
    ),
    upgrade_target: str | None = typer.Option(
        None,
        "--upgrade-target",
        help="upgrade chain の到達 HarnessOps version。既定は現在の runtime。",
    ),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """HarnessOps 管理状態を現在の hops 実装に合わせて更新または検証します。"""
    if upgrade_granularity not in GRANULARITIES:
        raise typer.BadParameter(f"--upgrade-granularity must be one of: {', '.join(sorted(GRANULARITIES))}")

    root = find_root()
    project = load_project(root)
    chain_args = _chain_passthrough_args(
        apply_migrations=apply_migrations,
        force=force,
        agent_bridge=agent_bridge,
        codex=codex,
        claude=claude,
        force_agent_bridge=force_agent_bridge,
    )
    intermediate_chain_args = _chain_passthrough_args(
        apply_migrations=apply_migrations,
        force=force,
        agent_bridge=False,
        codex=False,
        claude=False,
        force_agent_bridge=False,
    )
    chain_plan = build_upgrade_plan(
        root,
        target_version=upgrade_target,
        granularity=upgrade_granularity,
        extra_args=chain_args,
        intermediate_args=intermediate_chain_args,
    )
    chain_runs: list[UpgradeRun] = []

    if plan_upgrade:
        if json_output:
            typer.echo(json.dumps({"upgrade_chain": chain_plan.as_dict()}, ensure_ascii=False, indent=2, sort_keys=True))
        else:
            _echo_upgrade_plan(chain_plan)
        return

    if apply_upgrade_chain:
        chain_runs = run_upgrade_chain(chain_plan, cwd=root)
        ok = all(run.returncode == 0 for run in chain_runs)
        if json_output:
            typer.echo(
                json.dumps(
                    {
                        "ok": ok,
                        "upgrade_chain": chain_plan.as_dict(),
                        "runs": [run.as_dict() for run in chain_runs],
                    },
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            _echo_upgrade_plan(chain_plan)
            _echo_upgrade_runs(chain_runs)
        if not ok:
            raise typer.Exit(1)
        return

    auto_chain_steps = []
    if (
        upgrade_chain
        and not dry_run
        and not upgrade_chain_active()
        and chain_plan.needed
        and (upgrade_target is None or upgrade_target == __version__)
    ):
        auto_chain_steps = [step for step in chain_plan.steps if step.version != __version__]
        if auto_chain_steps:
            auto_plan = UpgradePlan(
                recorded_version=chain_plan.recorded_version,
                current_version=chain_plan.current_version,
                target_version=chain_plan.target_version,
                latest_pypi_version=chain_plan.latest_pypi_version,
                granularity=chain_plan.granularity,
                steps=auto_chain_steps,
                available_versions=chain_plan.available_versions,
                reason=chain_plan.reason,
            )
            chain_runs = run_upgrade_chain(auto_plan, cwd=root)
            if not all(run.returncode == 0 for run in chain_runs):
                if json_output:
                    typer.echo(
                        json.dumps(
                            {
                                "ok": False,
                                "upgrade_chain": auto_plan.as_dict(),
                                "runs": [run.as_dict() for run in chain_runs],
                            },
                            ensure_ascii=False,
                            indent=2,
                            sort_keys=True,
                        )
                    )
                else:
                    _echo_upgrade_plan(auto_plan)
                    _echo_upgrade_runs(chain_runs)
                raise typer.Exit(1)

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
    gitignore_result = ensure_gitignore(root, dry_run=dry_run)
    if not dry_run:
        refresh_views(root, project.overlay_path)

    existing_codex = (
        root / ".agents" / "skills" / "harnessops-bridge" / "SKILL.md"
    ).exists()
    existing_claude = (
        root / ".claude" / "skills" / "harnessops-bridge" / "SKILL.md"
    ).exists()
    refresh_codex = codex or existing_codex or (agent_bridge and not claude)
    refresh_claude = claude or existing_claude

    agent_result: dict[str, Any] = {
        "checked": [],
        "updated": [],
        "unchanged": [],
        "conflicted": [],
        "retired": [],
        "retained": [],
        "written_new": [],
        "managed_files": {},
    }
    if refresh_codex or refresh_claude:
        if dry_run:
            agent_result = refresh_bridge_files(
                root,
                codex=refresh_codex,
                claude=refresh_claude,
                force=force_agent_bridge,
                dry_run=True,
                github_flow=False if no_github_flow else None,
            )
        else:
            agent_result = refresh_bridge_files(
                root,
                codex=refresh_codex,
                claude=refresh_claude,
                force=force_agent_bridge,
                github_flow=False if no_github_flow else None,
            )

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
        "gitignore": gitignore_result,
        "agent_bridge": {
            "refreshed": bool(agent_result["checked"]),
            "github_flow": "disabled" if no_github_flow else "project-config",
            "paths": agent_result["checked"],
            "updated": agent_result["updated"],
            "unchanged": agent_result["unchanged"],
            "conflicted": agent_result["conflicted"],
            "retired": agent_result["retired"],
            "retained": agent_result["retained"],
            "written_new": agent_result["written_new"],
        },
        "doctor": report,
        "upgrade_chain": {
            "plan": chain_plan.as_dict(),
            "auto_applied": [run.as_dict() for run in chain_runs],
        },
    }
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        prefix = "[dry-run] " if dry_run else ""
        if chain_runs:
            _echo_upgrade_plan(
                UpgradePlan(
                    recorded_version=chain_plan.recorded_version,
                    current_version=chain_plan.current_version,
                    target_version=chain_plan.target_version,
                    latest_pypi_version=chain_plan.latest_pypi_version,
                    granularity=chain_plan.granularity,
                    steps=auto_chain_steps,
                    available_versions=chain_plan.available_versions,
                    reason=chain_plan.reason,
                ),
                prefix=prefix,
            )
            _echo_upgrade_runs(chain_runs, prefix=prefix)
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
        if gitignore_result["updated"]:
            typer.echo(f"{prefix}gitignore: updated .gitignore")
        if agent_result["checked"]:
            typer.echo(f"{prefix}agent bridge: checked {len(agent_result['checked'])} paths")
            typer.echo(f"{prefix}agent bridge: updated {len(agent_result['updated'])}")
            for item in agent_result["updated"]:
                typer.echo(f"  updated: {item}")
            typer.echo(f"{prefix}agent bridge: unchanged {len(agent_result['unchanged'])}")
            for item in agent_result["unchanged"]:
                typer.echo(f"  unchanged: {item}")
            typer.echo(f"{prefix}agent bridge: conflicted {len(agent_result['conflicted'])}")
            for item in agent_result["conflicted"]:
                typer.echo(f"  conflicted: {item}")
            if agent_result["retired"]:
                typer.echo(f"{prefix}agent bridge: retired {len(agent_result['retired'])}")
                for item in agent_result["retired"]:
                    typer.echo(f"  retired: {item}")
            if agent_result["retained"]:
                typer.echo(f"{prefix}agent bridge: retained edited retired files {len(agent_result['retained'])}")
                for item in agent_result["retained"]:
                    typer.echo(f"  retained: {item}")
            if agent_result["written_new"]:
                typer.echo(f"{prefix}agent bridge: wrote {len(agent_result['written_new'])} .new file(s)")
                for item in agent_result["written_new"]:
                    typer.echo(f"  {item['new']}")
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
