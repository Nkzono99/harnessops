from __future__ import annotations

import typer

from harnessops import __version__
from harnessops.cli import (
    add_failure,
    agent,
    decide,
    detect,
    doctor,
    eval,
    feedback,
    init,
    lab,
    migrate,
    profiles,
    propose,
    report,
    route,
    update_harness,
)

app = typer.Typer(add_completion=False, no_args_is_help=True, help="HarnessOps のフィードバックルーティングと改善実験CLI。")


@app.command()
def version() -> None:
    """HarnessOps バージョンを表示します。"""
    typer.echo(__version__)


profiles.register(app)
detect.register(app)
init.register(app)
doctor.register(app)
migrate.register(app)
add_failure.register(app)
feedback.register(app)
lab.register(app)
propose.register(app)
eval.register(app)
decide.register(app)
report.register(app)
agent.register(app)
route.register(app)
update_harness.register(app)


if __name__ == "__main__":
    app()
