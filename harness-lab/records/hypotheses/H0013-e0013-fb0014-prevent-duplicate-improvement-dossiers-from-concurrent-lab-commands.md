---
id: H0013
record_type: hypothesis
created_at: '2026-05-13T02:11:32+09:00'
status: proposed
target_capability: lab_record_consistency
source_eval_case: E0013
---

# H0013: E0013-fb0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands の仮説

## 仮説

Improvement dossier creation should be source-feedback-idempotent and doctor should detect duplicate source_feedback mappings, so concurrent lab commands cannot silently leave two dossiers for one feedback record.

## メカニズム

A short per-source lock around create_or_update_improvement_dossier serializes dossier creation, while doctor validates improvements/IMP*.md and reports duplicate source_feedback values as record consistency errors.

## 最小実装

Add a file-based source_feedback lock for dossier creation, include improvement dossiers in doctor record validation, add duplicate source_feedback validation, and cover evidence_ref rendering in dossier investigation output.

## 代替案: 削除または統合

Only document that lab commands must be run serially, but Codex and other agents naturally parallelize tool calls, so documentation would not prevent the failure.

## 期待される利点

Lab state remains one dossier per feedback source, doctor catches preexisting duplicates, and investigation evidence is visible during review.

## 想定される欠点

The lock adds small runtime complexity and must avoid stale-lock deadlocks.

## 評価計画

Add tests that doctor rejects duplicate improvement dossiers and that repeated/parallel dossier creation returns one file; verify dossier investigation renders evidence refs; run focused CLI/core tests and full test suite.

## 中止基準

If the lock can deadlock normal lab commands or duplicate detection creates false positives for valid dossier relations, replace it with deterministic repair guidance only.
