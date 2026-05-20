---
id: IMP0040
record_type: improvement_dossier
created_at: '2026-05-21T03:15:23+09:00'
updated_at: '2026-05-21T03:27:12+09:00'
status: adopted
source_type: issue
scope: harnessops-core
maturity: adopted
relation: new
promotion_level: target-lab-case
source_feedback: FB0055
eval_cases:
- E0043
hypotheses:
- H0043
decisions:
- D0044
research_scans: []
classification:
  capability: unclassified
  failure_class: unclassified
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
investigation:
- created_at: '2026-05-21T03:27:11+09:00'
  kind: codebase
  summary: 'FB0055/IMP0040 is adopted with an implemented guard, but its capability and failure_class are still unclassified because the imported issue carried unclassified metadata. Keep this as low-risk queue hygiene: update-harness managed-artifact whitespace and newline churn should be classified before the next memory compaction or release note pass, without creating a new root record.'
  evidence_ref: harness-lab/improvements/IMP0040-fb0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn.md; harness-lab/records/feedback/FB0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn.md; harness-lab/views/improvements.md
links:
  issue_url: https://github.com/Nkzono99/harnessops/issues/39
---

# IMP0040: FB0055: update-harness should avoid .gitignore line-ending and whitespace churn

## Status

- status: adopted
- maturity: adopted
- source_type: issue
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0055`
- linked_records: `FB0055`, `E0043`, `H0043`, `D0044`

## Source Observation

Source: `harness-lab/records/feedback/FB0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn.md`

# FB0055: update-harness should avoid .gitignore line-ending and whitespace churn

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/39
author: Nkzono99
labels: bug, enhancement
created_at: 2026-05-20T01:08:47Z
updated_at: 2026-05-20T01:08:47Z

## Issue本文
## Summary

Transferred from runops issue #86: https://github.com/Nkzono99/runops/issues/86

After `hops update-harness`, runops observed a large `.gitignore` diff that appeared to be mostly line-ending churn rather than meaningful content change. `git diff --check` also reported trailing whitespace in generated/managed output, requiring manual cleanup.

For managed artifact updates, `.gitignore` and similar existing files should avoid needless line-ending or whitespace churn so reviews focus on real harness changes.

## Expected behavior

When `hops update-harness` touches existing files:

- Preserve the existing line-ending style, or skip the write when normalized content is unchanged.
- Do not emit trailing whitespace from managed templates.
- Detect and report generated/managed whitespace issues after update.

## Acceptance criteria

- If `.gitignore` content is unchanged, update-harness does not produce a large line-ending-only diff.
- Generated or managed files do not introduce trailing whitespace.
- Existing user-managed files receive only minimal real diffs.
- Update summary ideally reports `line ending preserved` or `unchanged due to normalized content match` when applicable.

## Evidence from target repo

In runops on 2026-05-16, `uvx --refresh-package harnessops --from harnessops hops update-harness` produced a large `.gitignore` diff and `git diff --check` flagged trailing whitespace. The runops lab records track this as `FB0012` / `E0012` / `H0012` / `IMP0012`, with decision `D0015` currently `needs-more-evidence` and guard path `harnessops-core:tests/test_harness/test_update_harness.py::test_update_harness_preserves_gitignore_newlines_and_skips_normalized_noop`.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。

## Target Capability

- capability: unclassified
- failure_class: unclassified

## Investigation

- 2026-05-21T03:27:11+09:00 [codebase] FB0055/IMP0040 is adopted with an implemented guard, but its capability and failure_class are still unclassified because the imported issue carried unclassified metadata. Keep this as low-risk queue hygiene: update-harness managed-artifact whitespace and newline churn should be classified before the next memory compaction or release note pass, without creating a new root record. (evidence: harness-lab/improvements/IMP0040-fb0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn.md; harness-lab/records/feedback/FB0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn.md; harness-lab/views/improvements.md)

## Research Scans

research scan はまだありません。


## Evaluation

### E0043: E0043: FB0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn を評価


- source: `harness-lab/records/eval-cases/E0043-fb0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn.md`

- capability: unclassified

- failure_class: unclassified

- manual_eval_yml: `harness-lab/views/eval-results/E0043-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0043-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=0, minimality=0, regression_risk=4, operator_burden=0, anti_theater=0, maintainability=0, privacy_sanitization_risk=0
- notes: Implemented byte-preserving .gitignore no-op detection and newline preservation. Validation passed: uv run pytest tests/test_cli/test_mvp_flow.py; git diff --check; hops doctor --check-overlay --check-records; hops migrate --check.


## Hypotheses

### H0043: H0043: E0043-fb0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn の仮説


Source: `harness-lab/records/hypotheses/H0043-e0043-fb0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn.md`


# H0043: E0043-fb0055-update-harness-should-avoid-gitignore-line-ending-and-whitespace-churn の仮説

## 仮説

Preserve .gitignore newline style and skip normalized no-op writes so update-harness only produces meaningful managed-artifact diffs.

## メカニズム

採用前に、提案変更が作用するメカニズムを明示してください。曖昧なプロセス追加や文書追加だけでは証拠として不十分です。

## 最小実装

紐づく評価ケースで評価できる最も狭い変更を実装してください。複雑さを減らせるなら、新しい抽象より削除または統合を優先します。

## 代替案: 削除または統合

新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。

## 期待される利点

紐づく評価ケース `E0043` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

`hops lab eval --case E0043 --manual` を実行し、採用判断を作る前に多軸スコアを記録する。

## 中止基準

紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。


## Evidence

`harness-lab/views/eval-results/E0043-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: https://github.com/Nkzono99/harnessops/issues/39

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0044: D0044: adopted H0043


Source: `harness-lab/records/decisions/D0044-adopted-h0043.md`


# D0044: adopted H0043

## 判断

adopted

## 理由

Implemented normalized .gitignore no-op detection and existing newline preservation for update-harness.

## 証拠

uv run pytest tests/test_cli/test_mvp_flow.py passed; git diff --check passed; hops doctor --check-overlay --check-records passed; hops migrate --check passed.

## 回帰リスク

Low: behavior is scoped to .gitignore write decisions and covered by byte-preserving CRLF no-op and CRLF repair tests.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py::test_update_harness_preserves_gitignore_newlines_and_skips_normalized_noop
