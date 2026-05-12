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

