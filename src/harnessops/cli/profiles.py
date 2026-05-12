from __future__ import annotations

import json

import typer

from harnessops.core import yamlio
from harnessops.profiles.registry import load_builtin_profiles, load_profile, profile_fingerprint

profiles_app = typer.Typer(help="Inspect HarnessOps profiles.")


@profiles_app.command("list")
def list_profiles(json_output: bool = typer.Option(False, "--json")) -> None:
    """List built-in profiles."""
    profiles = load_builtin_profiles()
    if json_output:
        typer.echo(json.dumps(sorted(profiles), indent=2))
        return
    for profile_id in sorted(profiles):
        typer.echo(profile_id)


@profiles_app.command("show")
def show_profile(profile_id: str, json_output: bool = typer.Option(False, "--json")) -> None:
    """Show a profile."""
    profile = load_profile(profile_id)
    public = {k: v for k, v in profile.items() if not k.startswith("_")}
    public["fingerprint"] = profile_fingerprint(profile)
    if json_output:
        typer.echo(json.dumps(public, indent=2, sort_keys=True))
    else:
        typer.echo(yamlio.safe_dump(public, sort_keys=False))


def register(app: typer.Typer) -> None:
    app.add_typer(profiles_app, name="profiles")
