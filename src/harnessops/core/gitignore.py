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


def _detect_newline(text: str) -> str:
    crlf_count = text.count("\r\n")
    lf_count = text.count("\n") - crlf_count
    return "\r\n" if crlf_count > lf_count else "\n"


def ensure_gitignore(root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    path = root / ".gitignore"
    original_text = path.read_bytes().decode("utf-8") if path.exists() else ""
    newline = _detect_newline(original_text)
    original = original_text.splitlines()
    block = _managed_block()
    managed_set = set(block)
    result: list[str] = []
    index = 0
    block_written = False

    while index < len(original):
        line = original[index]
        if line == BEGIN_MARKER:
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
            index += 1
            continue
        result.append(line)
        index += 1

    if not block_written:
        if result and result[-1] != "":
            result.append("")
        result.extend(block)

    while result and result[-1] == "":
        result.pop()

    changed = result != original
    if changed and not dry_run:
        path.write_bytes((newline.join(result) + newline).encode("utf-8"))

    return {
        "path": ".gitignore",
        "updated": changed,
        "patterns": MANAGED_PATTERNS,
        "line_ending": "crlf" if newline == "\r\n" else "lf",
        "reason": "updated" if changed else "normalized content unchanged",
    }
