from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


DEFAULT_PATTERNS = [
    (re.compile(r"/home/[^\s)\"']+"), "<LOCAL_PATH>"),
    (re.compile(r"/LARGE\d+/[^\s)\"']+"), "<LOCAL_PATH>"),
    (re.compile(r"cluster-[A-Za-z0-9_-]+"), "<CLUSTER>"),
]


def _load_sanitize_config(root: Path) -> dict[str, Any]:
    path = root / ".harnessops" / "sanitize.yml"
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def sanitize_text(text: str, *, root: Path, profile: dict[str, Any] | None = None, allow_private: bool = False) -> str:
    if allow_private:
        return text
    result = text.replace(root.as_posix(), "<PROJECT_ROOT>")
    for pattern, replacement in DEFAULT_PATTERNS:
        result = pattern.sub(replacement, result)
    config = _load_sanitize_config(root)
    for item in config.get("redact_patterns", []):
        result = re.sub(str(item["pattern"]), str(item.get("replacement", "<REDACTED>")), result)
    for term in config.get("private_terms", []):
        result = result.replace(str(term), "<PRIVATE_TERM>")
    for key in ["private_paths", "protected_paths"]:
        for pattern in (profile or {}).get(key, []) or []:
            literal = str(pattern).replace("**", "").replace("*", "")
            if literal and literal in result:
                result = result.replace(literal, "<PROTECTED_PATH>")
    result += "\n\n## Private info excluded\n\n- private info excluded\n- source project anonymized\n- local paths redacted\n"
    return result

