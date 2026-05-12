from __future__ import annotations

import typer

from harnessops import __version__
from harnessops.cli import add_failure, agent, decide, detect, doctor, eval, feedback, init, lab, migrate, profiles, propose, report, route

app = typer.Typer(no_args_is_help=True, help="HarnessOps feedback routing and improvement experiment CLI.")


@app.command()
def version() -> None:
    """Print HarnessOps version."""
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


if __name__ == "__main__":
    app()
