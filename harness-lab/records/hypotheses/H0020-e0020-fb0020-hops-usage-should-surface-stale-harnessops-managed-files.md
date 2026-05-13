---
id: H0020
record_type: hypothesis
created_at: '2026-05-13T17:02:04+09:00'
status: proposed
target_capability: harness_lab_traceability
source_eval_case: E0020
---

# H0020: E0020-fb0020-hops-usage-should-surface-stale-harnessops-managed-files の仮説

## 仮説

A pip-style low-noise update notice will make stale HarnessOps managed artifacts visible during normal hops usage without interrupting the user workflow.

## メカニズム

Compare the current harnessops package version with .harnessops/lock.json harnessops_version for linked repositories, throttle notice emission with a local cache, skip update-harness/version/help-like commands, and point agents to the hops-update-harness skill plus hops update-harness.

## 最小実装

Add a CLI callback or entry wrapper that runs a best-effort stale-lock notice before ordinary commands, stores last notice state under .harnessops/cache, and tests both notice and opt-out behavior.

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0020` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

Create a CLI regression test with an older lock harnessops_version that asserts a notice is emitted on ordinary hops usage and suppressed after a recent notice or while running update-harness.

## 中止基準

Reject if the notice appears on every command, breaks JSON output, blocks commands on errors, or requires network access.
