from __future__ import annotations

import importlib.resources
import json
from typing import Any


def load_schema(name: str) -> dict[str, Any]:
    text = importlib.resources.files("harnessops.schemas.json").joinpath(name).read_text(encoding="utf-8")
    return json.loads(text)

