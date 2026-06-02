from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

import tomli_w

from harnessops.core.paths import join_display_path, resolve_overlay_path


@dataclass(frozen=True)
class Project:
    root: Path
    data: dict[str, Any]
    state_root: Path | None = None
    project_file_path: Path | None = None
    registry_id: str | None = None

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
    def overlay_storage(self) -> str:
        return str(self.data.get("overlay", {}).get("storage", "repo"))

    @property
    def storage_root(self) -> Path:
        return self.state_root or self.root

    @property
    def overlay_dir(self) -> Path:
        return resolve_overlay_path(self.storage_root, self.overlay_path)

    @property
    def metadata_root(self) -> Path:
        return self.storage_root

    def display_path(self, path: Path) -> str:
        resolved = path.resolve()
        if self.overlay_storage != "local":
            try:
                relative = resolved.relative_to(self.overlay_dir)
                return join_display_path(self.overlay_path, relative)
            except ValueError:
                pass
        try:
            return resolved.relative_to(self.root.resolve()).as_posix()
        except ValueError:
            return resolved.as_posix()


def project_file(root: Path) -> Path:
    return root / ".harnessops" / "project.toml"


def load_project(root: Path) -> Project:
    path = project_file(root)
    if path.exists():
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        storage = str(data.get("overlay", {}).get("storage", "repo"))
        state_root = root
        if storage == "local":
            local_state_root = data.get("overlay", {}).get("state_root")
            local_id = data.get("overlay", {}).get("local_id")
            if local_state_root:
                state_root = Path(str(local_state_root)).expanduser().resolve()
            elif local_id:
                from harnessops.core.registry import local_project_state_root

                state_root = local_project_state_root(str(local_id))
        return Project(root=root, data=data, state_root=state_root, project_file_path=path)

    from harnessops.core.registry import load_registered_project

    registered = load_registered_project(root)
    if registered is not None:
        return registered
    raise FileNotFoundError(f"HarnessOps プロジェクトがリンクされていません: {path}")


def write_project(root: Path, data: dict[str, Any]) -> None:
    path = project_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(tomli_w.dumps(data), encoding="utf-8")
