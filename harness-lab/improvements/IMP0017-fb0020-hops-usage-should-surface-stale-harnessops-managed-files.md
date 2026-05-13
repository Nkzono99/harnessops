---
id: IMP0017
record_type: improvement_dossier
created_at: '2026-05-13T17:01:41+09:00'
updated_at: '2026-05-13T17:07:37+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: target-lab-case
source_feedback: FB0020
eval_cases:
- E0020
hypotheses:
- H0020
decisions:
- D0021
research_scans: []
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once
investigation:
- created_at: '2026-05-13T17:01:51+09:00'
  kind: external-benchmark
  summary: 'pip implements its update notice as a CLI wrapper around command execution: fetch a potential prompt before the command, cache remote version state for roughly one week, skip when disabled/no-index, then emit the notice after the command body without failing the command if the check errors.'
  evidence_ref: https://github.com/pypa/pip/blob/main/src/pip/_internal/cli/index_command.py
links:
  issue_url:
---

# IMP0017: FB0020: hops usage should surface stale HarnessOps managed files

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0020`
- linked_records: `FB0020`, `E0020`, `H0020`, `D0021`

## Source Observation

Source: `harness-lab/records/feedback/FB0020-hops-usage-should-surface-stale-harnessops-managed-files.md`

# FB0020: hops usage should surface stale HarnessOps managed files

## 概要

After a HarnessOps release, linked repositories can keep older generated skills or managed artifacts until update-harness runs. Users may keep using hops without noticing that update-harness should be applied.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

When a linked repository is used with a newer hops version than the recorded lock state, hops should emit a low-noise notice that points the user or agent to the hops-update-harness skill / hops update-harness.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

- 2026-05-13T17:01:51+09:00 [external-benchmark] pip implements its update notice as a CLI wrapper around command execution: fetch a potential prompt before the command, cache remote version state for roughly one week, skip when disabled/no-index, then emit the notice after the command body without failing the command if the check errors. (evidence: https://github.com/pypa/pip/blob/main/src/pip/_internal/cli/index_command.py)

## Research Scans

research scan はまだありません。


## Evaluation

### E0020: E0020: FB0020-hops-usage-should-surface-stale-harnessops-managed-files を評価


- source: `harness-lab/records/eval-cases/E0020-fb0020-hops-usage-should-surface-stale-harnessops-managed-files.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0020-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0020-manual-score.md`
- scores: impact=4, mechanism_clarity=4, evaluability=5, minimality=4, regression_risk=2, operator_burden=1, anti_theater=4, maintainability=4, privacy_sanitization_risk=1
- notes: Focused regression tests show stale harnessops_version emits a hops-update-harness notice once and suppresses it for update-harness itself; a real doctor run in this repository surfaced the stale 0.1.2 -> 0.1.3 lock.


## Hypotheses

### H0020: H0020: E0020-fb0020-hops-usage-should-surface-stale-harnessops-managed-files の仮説


Source: `harness-lab/records/hypotheses/H0020-e0020-fb0020-hops-usage-should-surface-stale-harnessops-managed-files.md`


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


## Evidence

`harness-lab/views/eval-results/E0020-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0021: D0021: adopted H0020


Source: `harness-lab/records/decisions/D0021-adopted-h0020.md`


# D0021: adopted H0020

## 判断

adopted

## 理由

Adopted after focused tests and a real stale-lock doctor run confirmed the low-noise update-harness notice behavior.

## 証拠

Focused pytest cases and repo-local doctor output showing 0.1.2 -> 0.1.3 notice.

## 回帰リスク

Low; notice is best-effort, cached for seven days, stderr-only, and suppressed for update-harness/version.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once
