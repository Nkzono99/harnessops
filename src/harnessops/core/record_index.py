from __future__ import annotations

from pathlib import Path
import re

from harnessops.core.project import Project
from harnessops.core.record_io import read_record, slugify
from harnessops.core.record_types import ID_PREFIXES, RECORD_DIRS


def next_id(directory: Path, prefix: str) -> str:
    directory.mkdir(parents=True, exist_ok=True)
    max_id = 0
    pattern = re.compile(rf"^{re.escape(prefix)}(\d{{4}})")
    for path in directory.glob(f"{prefix}[0-9][0-9][0-9][0-9]*.md"):
        match = pattern.match(path.name)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return f"{prefix}{max_id + 1:04d}"


def record_path(project: Project, record_type: str, record_id: str, title: str) -> Path:
    rel_dir = RECORD_DIRS[record_type]
    return project.overlay_dir / rel_dir / f"{record_id}-{slugify(title)}.md"


def _canonical_record_dirs(record_or_path: str) -> list[Path]:
    dirs: list[Path] = []
    for record_type, prefix in sorted(ID_PREFIXES.items(), key=lambda item: len(item[1]), reverse=True):
        if record_or_path.startswith(prefix):
            dirs.append(Path(RECORD_DIRS[record_type]))
    return dirs


def find_record(project: Project, record_or_path: str) -> Path:
    candidate = Path(record_or_path)
    if candidate.exists():
        return candidate
    for rel_dir in _canonical_record_dirs(record_or_path):
        directory = project.overlay_dir / rel_dir
        for path in sorted(directory.glob(f"{record_or_path}*.md")):
            return path
    for path in project.overlay_dir.rglob("*.md"):
        if path.name.startswith(record_or_path):
            return path
        frontmatter, _ = read_record(path)
        if frontmatter.get("id") == record_or_path:
            return path
    raise FileNotFoundError(f"レコードが見つかりません: {record_or_path}")
