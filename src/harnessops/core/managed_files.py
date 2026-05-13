from __future__ import annotations

from pathlib import Path


def conflict_path(path: Path, text: str) -> Path:
    candidate = path.with_name(path.name + ".new")
    if not candidate.exists() or candidate.read_text(encoding="utf-8") == text:
        return candidate
    index = 1
    while True:
        numbered = path.with_name(f"{path.name}.new.{index}")
        if not numbered.exists() or numbered.read_text(encoding="utf-8") == text:
            return numbered
        index += 1
