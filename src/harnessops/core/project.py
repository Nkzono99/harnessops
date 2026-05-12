from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

import tomli_w


@dataclass(frozen=True)
class Project:
    root: Path
    data: dict[str, Any]

    @property
    def profile_id(self) -> str:
        return str(self.data.get("profile", {}).get("id", ""))

    @property
    def overlay_mode(self) -> str:
        return str(self.data.get("overlay", {}).get("mode", ""))

    @property
    def overlay_path(self) -> str:
        return str(self.data.get("overlay", {}).get("path", ""))

    @property
    def overlay_dir(self) -> Path:
        return self.root / self.overlay_path


def project_file(root: Path) -> Path:
    return root / ".harnessops" / "project.toml"


def load_project(root: Path) -> Project:
    path = project_file(root)
    if not path.exists():
        raise FileNotFoundError(f"HarnessOps project is not linked: {path}")
    return Project(root=root, data=tomllib.loads(path.read_text(encoding="utf-8")))


def write_project(root: Path, data: dict[str, Any]) -> None:
    path = project_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(tomli_w.dumps(data), encoding="utf-8")

