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
    if any(token in lowered for token in ["do not upstream", "private only", "local only", "do-not-upstream", "上流化しない", "非公開のみ", "ローカルのみ"]):
        disposition = "do-not-upstream"
    elif any(token in lowered for token in [".harness/manifest", "common manifest", "protocol", "cli convention", "共通マニフェスト", "プロトコル", "cli規約"]):
        disposition = "protocol-candidate"
    elif target and target != "harnessops" and not any(token in lowered for token in ["research direction", "paper claim", "experiment direction", "project evolution", "研究方針", "論文主張", "実験方針", "プロジェクト発展"]):
        disposition = "target-upstream-candidate"
    elif any(token in lowered for token in ["harnessops", "meta-harness", "schema", "overlay", "plugin", "migration", "hops cli", "メタハーネス", "スキーマ", "オーバーレイ", "プラグイン", "マイグレーション"]):
        disposition = "meta-harness-candidate"
    elif any(token in lowered for token in ["cluster", "slurm", "journal", "simulator", "external", "クラスタ", "ジャーナル", "シミュレータ", "外部"]):
        disposition = "external-candidate"
    elif any(token in lowered for token in ["research direction", "paper claim", "experiment direction", "project evolution", "pivot", "研究方針", "論文主張", "実験方針", "プロジェクト発展", "方針転換"]):
        disposition = "project-evolution"
    elif any(token in lowered for token in ["workaround", "local process", "project-specific", "回避策", "ローカルプロセス", "プロジェクト固有"]):
        disposition = "project-local-process"
    else:
        disposition = "target-upstream-candidate"
    if target == "harnessops":
        disposition = "meta-harness-candidate"
    elif target and disposition == "meta-harness-candidate":
        disposition = "target-upstream-candidate"
    return {"type": disposition, "target": target if disposition in {"target-upstream-candidate", "meta-harness-candidate"} else None, "status": "draft"}
