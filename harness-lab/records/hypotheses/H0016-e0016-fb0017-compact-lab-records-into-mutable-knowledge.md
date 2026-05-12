---
id: H0016
record_type: hypothesis
created_at: '2026-05-13T02:53:18+09:00'
status: proposed
target_capability: lab_memory_compaction
source_eval_case: E0016
---

# H0016: E0016-fb0017-compact-lab-records-into-mutable-knowledge の仮説

## 仮説

A hops lab compact command can keep long-running lab work usable by compiling canonical records into source-linked mutable knowledge files.

## メカニズム

The command measures lab size, exits without writing until thresholds are exceeded unless forced, then updates a compact knowledge map from feedback, dossier, decision, score, guard, and investigation metadata. Canonical records remain the audit log; knowledge files become the mutable working memory.

## 最小実装

Add a deterministic compaction core, a hops lab compact CLI with threshold and force options, docs/spec coverage, and tests that verify threshold gating, source links, scores, guards, and doctor compatibility.

## 代替案: 削除または統合

Do not archive or delete records first. Avoid adding another append-only record family; use a regenerated mutable knowledge layer with source hashes and timestamps.

## 期待される利点

Agents and humans can consult a compact lab memory once harness-lab grows, while still being able to trace every knowledge item back to records and dossiers.

## 想定される欠点

A stale or overconfident summary could hide important contradictions, so the output must preserve source IDs, threshold metadata, and warnings rather than replacing records.

## 評価計画

Run focused CLI tests for forced compaction and threshold skip behavior, then full pytest, ruff, doctor, and migrate checks.

## 中止基準

Reject or park if the command mutates canonical records, drops source traceability, requires network or model calls, or makes doctor fail on generated knowledge files.
