from __future__ import annotations

import click
import typer


def current_command_path() -> str:
    ctx = click.get_current_context(silent=True)
    parts: list[str] = []
    while ctx is not None:
        if ctx.info_name:
            parts.append(str(ctx.info_name))
        ctx = ctx.parent
    return " ".join(reversed(parts))


def warn_if_deprecated(deprecated_suffix: str, replacement: str) -> None:
    path = current_command_path()
    suffix_parts = deprecated_suffix.split()
    path_parts = path.split()
    matches = path_parts == suffix_parts
    matches_with_binary = (
        len(path_parts) == len(suffix_parts) + 1
        and path_parts[1:] == suffix_parts
    )
    if not matches and not matches_with_binary:
        return
    typer.echo(
        f"DEPRECATED: `{deprecated_suffix}` is deprecated; use `{replacement}`.",
        err=True,
    )
