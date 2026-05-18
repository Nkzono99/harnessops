from __future__ import annotations

import typer

from harnessops import __version__
from harnessops.cli import (
    add_failure,
    agent,
    codex_plugin,
    decide,
    detect,
    doctor,
    eval,
    feedback,
    github_flow,
    init,
    lab,
    migrate,
    local,
    profiles,
    project,
    propose,
    report,
    route,
    steward,
    update_harness,
)

app = typer.Typer(add_completion=False, no_args_is_help=True, help="HarnessOps のフィードバックルーティングと改善実験CLI。")


@app.callback()
def main_callback(
    ctx: typer.Context,
    disable_update_notice: bool = typer.Option(
        False,
        "--disable-update-notice",
        envvar="HOPS_DISABLE_UPDATE_NOTICE",
        help="HarnessOps 管理物の更新 notice を表示しません。",
    ),
) -> None:
    """Run lightweight cross-command CLI hooks."""
    from harnessops.cli.update_notice import maybe_emit_update_notice

    if disable_update_notice:
        return
    maybe_emit_update_notice(ctx.invoked_subcommand)


@app.command()
def version() -> None:
    """HarnessOps バージョンを表示します。"""
    typer.echo(__version__)


profiles.register(app)
detect.register(app)
init.register(app)
doctor.register(app)
migrate.register(app)
project.register(app)
local.register(app)
add_failure.register(app)
feedback.register(app)
lab.register(app)
propose.register(app)
eval.register(app)
decide.register(app)
report.register(app)
agent.register(app)
codex_plugin.register(app)
route.register(app)
github_flow.register(app)
steward.register(app)
update_harness.register(app)


if __name__ == "__main__":
    app()
