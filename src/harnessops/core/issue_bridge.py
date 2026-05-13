from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from harnessops.core import yamlio
from harnessops.core.sanitize import DEFAULT_PATTERNS


INVALID_REPO_MESSAGE = "--repo は owner/repo 形式で指定してください"


def validate_repo(repo: str) -> None:
    parts = repo.split("/")
    if len(parts) != 2 or not all(parts) or any(char.isspace() for char in repo):
        raise ValueError(INVALID_REPO_MESSAGE)


def configured_private_terms(root: Path) -> list[str]:
    path = root / ".harnessops" / "sanitize.yml"
    if not path.exists():
        return []
    config = yamlio.safe_load(path.read_text(encoding="utf-8")) or {}
    return [str(term) for term in config.get("private_terms", [])]


def remaining_private_markers(
    root: Path, profile: dict[str, Any], body: str
) -> list[str]:
    markers: list[str] = []
    for root_text in {str(root), root.as_posix()}:
        if root_text and root_text in body:
            markers.append("project-root")
    for pattern, _ in DEFAULT_PATTERNS:
        if pattern.search(body):
            markers.append(pattern.pattern)
    for term in configured_private_terms(root):
        if term and term in body:
            markers.append("private-term")
    for key in ["private_paths", "protected_paths"]:
        for pattern in profile.get(key, []) or []:
            literal = str(pattern).replace("**", "").replace("*", "")
            if literal and literal in body:
                markers.append(key)
    return sorted(set(markers))


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        check=True,
        capture_output=True,
        text=True,
    )


def search_duplicate_issues(
    repo: str, title: str
) -> tuple[list[dict[str, Any]], str | None]:
    try:
        result = run_gh(
            [
                "issue",
                "list",
                "--repo",
                repo,
                "--state",
                "open",
                "--search",
                f"{title} in:title",
                "--limit",
                "5",
                "--json",
                "number,title,url,state",
            ]
        )
        payload = json.loads(result.stdout)
    except FileNotFoundError:
        return [], "gh が見つかりません"
    except (json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        return [], f"GitHub Issue検索に失敗しました: {exc}"
    if not isinstance(payload, list):
        return [], "GitHub Issue検索の応答形式が不正です"
    return [item for item in payload if isinstance(item, dict)], None


def create_github_issue(repo: str, title: str, body: str) -> str:
    try:
        result = run_gh(
            [
                "issue",
                "create",
                "--repo",
                repo,
                "--title",
                title,
                "--body",
                body,
            ]
        )
    except FileNotFoundError as exc:
        raise RuntimeError("gh が見つかりません") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or str(exc)
        raise RuntimeError(f"GitHub Issue作成に失敗しました: {message}") from exc
    url = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""
    if not url.startswith("https://"):
        raise RuntimeError("GitHub Issue URLを取得できませんでした")
    return url
