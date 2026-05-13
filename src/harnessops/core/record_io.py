from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any

from harnessops.core import yamlio


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug or "record"


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    data = yamlio.safe_load(parts[1]) or {}
    return data, parts[2]


def dump_record(frontmatter: dict[str, Any], body: str) -> str:
    yaml_text = yamlio.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)
    return f"---\n{yaml_text}---\n\n{body.strip()}\n"


def read_record(path: Path) -> tuple[dict[str, Any], str]:
    return split_frontmatter(path.read_text(encoding="utf-8"))
