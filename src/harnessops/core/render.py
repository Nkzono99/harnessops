from __future__ import annotations

from pathlib import Path

from harnessops.core.overlay import GENERATED_MARKER
from harnessops.core.records import read_record


def refresh_views(root: Path, overlay_rel: str) -> list[Path]:
    overlay = root / overlay_rel
    written: list[Path] = []
    if overlay.name == "harness-feedback":
        failures = []
        for path in sorted((overlay / "records/failures").glob("*.md")):
            frontmatter, _ = read_record(path)
            disposition = frontmatter.get("disposition", {})
            failures.append(f"- `{frontmatter.get('id')}` {disposition.get('type')} -> {disposition.get('target')}\n")
        view = overlay / "views" / "open-routing.md"
        view.write_text(GENERATED_MARKER + "# Open Routing\n\n" + ("".join(failures) or "No failure records yet.\n"), encoding="utf-8")
        written.append(view)
    else:
        rows = []
        for path in sorted((overlay / "records/feedback").glob("*.md")):
            frontmatter, _ = read_record(path)
            classification = frontmatter.get("classification", {})
            rows.append(
                f"- `{frontmatter.get('id')}` {frontmatter.get('status')} "
                f"{classification.get('capability')} {classification.get('failure_class')}\n"
            )
        view = overlay / "views" / "imported-feedback.md"
        view.write_text(GENERATED_MARKER + "# Imported Feedback\n\n" + ("".join(rows) or "No imported feedback records yet.\n"), encoding="utf-8")
        written.append(view)
    return written

