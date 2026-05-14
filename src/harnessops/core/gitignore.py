from __future__ import annotations

from pathlib import Path
from typing import Any

BEGIN_MARKER = "# BEGIN harnessops"
END_MARKER = "# END harnessops"

MANAGED_PATTERNS = [
    ".harnessops/cache/*",
    "!.harnessops/cache/.gitkeep",
    ".harnessops/tmp/",
]


def _managed_block() -> list[str]:
    return [BEGIN_MARKER, *MANAGED_PATTERNS, END_MARKER]


def ensure_gitignore(root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    path = root / ".gitignore"
    original = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    block = _managed_block()
    managed_set = set(block)
    result: list[str] = []
    changed = False
    index = 0
    block_written = False

    while index < len(original):
        line = original[index]
        if line == BEGIN_MARKER:
            changed = True
            while index < len(original) and original[index] != END_MARKER:
                index += 1
            if index < len(original):
                index += 1
            if result and result[-1] != "":
                result.append("")
            result.extend(block)
            block_written = True
            continue
        if line in managed_set:
            changed = True
            index += 1
            continue
        result.append(line)
        index += 1

    if not block_written:
        if result and result[-1] != "":
            result.append("")
        result.extend(block)
        changed = True

    while result and result[-1] == "":
        result.pop()

    if changed and not dry_run:
        path.write_text("\n".join(result) + "\n", encoding="utf-8", newline="\n")

    return {
        "path": ".gitignore",
        "updated": changed,
        "patterns": MANAGED_PATTERNS,
    }
