from __future__ import annotations

from pathlib import Path


def find_root(start: Path | None = None) -> Path:
    """Return the repository root used by HarnessOps commands."""
    root = (start or Path.cwd()).resolve()
    for candidate in [root, *root.parents]:
        if (candidate / ".harnessops" / "project.toml").exists():
            return candidate
        if (candidate / ".git").exists():
            return candidate
    return root


def relpath(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def resolve_project_path(root: Path, path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return root / candidate


def resolve_overlay_path(root: Path, overlay_path: str) -> Path:
    return resolve_project_path(root, overlay_path).resolve()


def join_display_path(base: str, *parts: str | Path) -> str:
    path = Path(base)
    for part in parts:
        path /= part
    return path.as_posix()


def display_path(path: Path, root: Path) -> str:
    try:
        return relpath(path, root)
    except ValueError:
        return path.resolve().as_posix()


def display_overlay_file(root: Path, overlay_path: str, path: Path) -> str:
    overlay_dir = resolve_overlay_path(root, overlay_path)
    try:
        relative = path.resolve().relative_to(overlay_dir)
    except ValueError:
        return display_path(path, root)
    return join_display_path(overlay_path, relative)
