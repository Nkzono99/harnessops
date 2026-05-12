from __future__ import annotations

from io import StringIO
from typing import Any

try:
    import yaml as _pyyaml  # type: ignore[import-untyped]
except ModuleNotFoundError:  # pragma: no cover - exercised in packaged uv env
    _pyyaml = None


def safe_load(text: str) -> Any:
    if _pyyaml is not None:
        return _pyyaml.safe_load(text)
    from ruamel.yaml import YAML

    parser = YAML(typ="safe")
    return parser.load(text)


def safe_dump(data: Any, *, sort_keys: bool = False, allow_unicode: bool = False) -> str:
    if _pyyaml is not None:
        return _pyyaml.safe_dump(data, sort_keys=sort_keys, allow_unicode=allow_unicode, width=4096)
    from ruamel.yaml import YAML

    output = StringIO()
    dumper = YAML()
    dumper.default_flow_style = False
    dumper.allow_unicode = allow_unicode
    dumper.width = 4096
    if sort_keys:
        data = _sort_mapping(data)
    dumper.dump(data, output)
    return output.getvalue()


def _sort_mapping(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _sort_mapping(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_sort_mapping(item) for item in value]
    return value
