from __future__ import annotations

import shutil
from pathlib import Path

import pytest


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def copy_fixture(tmp_path: Path, repo_root: Path):
    def _copy(name: str) -> Path:
        source = repo_root / "tests" / "fixtures" / name
        target = tmp_path / name
        shutil.copytree(source, target)
        return target

    return _copy

