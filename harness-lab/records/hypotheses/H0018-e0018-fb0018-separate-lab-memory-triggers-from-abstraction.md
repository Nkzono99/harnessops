---
id: H0018
record_type: hypothesis
created_at: '2026-05-13T09:28:24+09:00'
status: proposed
target_capability: lab_memory_compaction
source_eval_case: E0018
---

# H0018: E0018-fb0018-separate-lab-memory-triggers-from-abstraction の仮説

## 仮説

Separating lab memory lint/prepare from deterministic snapshots lets HarnessOps preserve auditable indexes while allowing agent skills to perform higher-level semantic compaction.

## メカニズム

A non-writing lint command detects pressure and stale/missing memory state; prepare emits a source-linked input bundle; the hops-compact-lab-memory skill updates abstract knowledge with source IDs and source digests.

## 最小実装

Add lab memory lint/prepare CLI paths, a compaction skill, docs, and contract tests while keeping hops lab compact as a deterministic snapshot.

## 代替案: 削除または統合

Remove the deterministic snapshot entirely and rely only on a skill, but that loses cheap machine-readable source indexes and digest checks.

## 期待される利点

紐づく評価ケース `E0018` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

Run targeted CLI and bridge tests, full pytest, ruff, doctor, migrate, and confirm lint/prepare behavior on the live lab.

## 中止基準

Revert or simplify if lint cannot produce actionable triggers, if generated bundles encourage unsourced abstractions, or if the new skill duplicates existing run-lab duties without clearer boundaries.
