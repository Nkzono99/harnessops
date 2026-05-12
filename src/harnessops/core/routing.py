from __future__ import annotations

from typing import Any

DISPOSITIONS = {
    "project-evolution",
    "project-local-process",
    "target-upstream-candidate",
    "meta-harness-candidate",
    "protocol-candidate",
    "external-candidate",
    "do-not-upstream",
}


def classify_text(text: str, *, target: str | None = None) -> dict[str, Any]:
    lowered = text.lower()
    if any(token in lowered for token in ["do not upstream", "private only", "local only", "do-not-upstream"]):
        disposition = "do-not-upstream"
    elif any(token in lowered for token in [".harness/manifest", "common manifest", "protocol", "cli convention"]):
        disposition = "protocol-candidate"
    elif target and target != "harnessops" and not any(token in lowered for token in ["research direction", "paper claim", "experiment direction", "project evolution"]):
        disposition = "target-upstream-candidate"
    elif any(token in lowered for token in ["harnessops", "meta-harness", "schema", "overlay", "plugin", "migration", "hops cli"]):
        disposition = "meta-harness-candidate"
    elif any(token in lowered for token in ["cluster", "slurm", "journal", "simulator", "external"]):
        disposition = "external-candidate"
    elif any(token in lowered for token in ["research direction", "paper claim", "experiment direction", "project evolution", "pivot"]):
        disposition = "project-evolution"
    elif any(token in lowered for token in ["workaround", "local process", "project-specific"]):
        disposition = "project-local-process"
    else:
        disposition = "target-upstream-candidate"
    if target == "harnessops":
        disposition = "meta-harness-candidate"
    elif target and disposition == "meta-harness-candidate":
        disposition = "target-upstream-candidate"
    return {"type": disposition, "target": target if disposition in {"target-upstream-candidate", "meta-harness-candidate"} else None, "status": "draft"}
