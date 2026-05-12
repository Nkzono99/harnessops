---
id: IMP0013
record_type: improvement_dossier
created_at: '2026-05-13T02:32:03+09:00'
updated_at: '2026-05-13T02:42:14+09:00'
status: adopted
source_type: user-review
scope: harnessops-core
maturity: adopted
relation: new
promotion_level: target-lab-case
source_feedback: FB0016
eval_cases:
- E0015
hypotheses:
- H0015
decisions:
- D0016
classification:
  capability: lab_evaluation_review
  failure_class: eval_template_noise_in_dossier
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
investigation: []
links:
  issue_url:
---

# IMP0013: FB0016: Remove unused eval-case template noise from dossiers

## Status

- status: adopted
- maturity: adopted
- source_type: user-review
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0016`
- linked_records: `FB0016`, `E0015`, `H0015`, `D0016`

## Source Observation

Source: `harness-lab/records/feedback/FB0016-remove-unused-eval-case-template-noise-from-dossiers.md`

# FB0016: Remove unused eval-case template noise from dossiers

## 概要

Improvement dossiers render the full eval_case record body under ## Evaluation, so readers see generic sections like fixtures, task, expected behavior, pass/fail criteria that often remain template text. Manual eval yml results are the part that actually functions.

## 再現

Open harness-lab/improvements/IMP*.md and inspect ## Evaluation. It embeds # E000*: ## フィクスチャ, ## タスク, ## 期待される挙動 and similar sections even when they are template text.

## 期待する上流変更

Either make eval cases meaningful in the flow or stop rendering template bodies into dossiers. Prefer summarizing eval records and manual score outputs in dossiers, and generate more source-specific eval case text for new cases.

## Target Capability

- capability: lab_evaluation_review
- failure_class: eval_template_noise_in_dossier

## Investigation

調査メモはまだありません。

## Evaluation

### E0015: E0015: FB0016-remove-unused-eval-case-template-noise-from-dossiers を評価


- source: `harness-lab/records/eval-cases/E0015-fb0016-remove-unused-eval-case-template-noise-from-dossiers.md`

- capability: lab_evaluation_review

- failure_class: eval_template_noise_in_dossier

- manual_eval_yml: `harness-lab/views/eval-results/E0015-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0015-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=2, operator_burden=5, anti_theater=5, maintainability=4, privacy_sanitization_risk=5
- notes: Dossiers now summarize eval records and manual eval yml/md instead of embedding full eval-case template bodies. New eval cases are seeded from source feedback summary, reproduction, and expected change. Manual eval markdown no longer includes a full eval case snapshot.


## Hypotheses

### H0015: H0015: E0015-fb0016-remove-unused-eval-case-template-noise-from-dossiers の仮説


Source: `harness-lab/records/hypotheses/H0015-e0015-fb0016-remove-unused-eval-case-template-noise-from-dossiers.md`


# H0015: E0015-fb0016-remove-unused-eval-case-template-noise-from-dossiers の仮説

## 仮説

Dossiers should summarize evaluation records and score outputs instead of embedding full eval-case template bodies, while new eval cases should be seeded from source feedback so the canonical record is useful when opened directly.

## メカニズム

A compact evaluation summary points reviewers to source records and manual-score yml/md, eliminating stale template text from the main review surface. Source-specific eval case generation keeps the underlying record meaningful enough for scoring and later inspection.

## 最小実装

Change dossier rendering to use an evaluation summary, remove full eval-case snapshots from manual eval markdown, seed new eval cases from feedback summary/reproduction/expected-change, update tests and docs.

## 代替案: 削除または統合

Delete eval_case records entirely and rely only on manual eval yml, but that removes the hook used by hypotheses and decisions.

## 期待される利点

harness-lab/improvements becomes readable, yml score outputs remain the functional evaluation artifact, and new eval cases stop starting from generic filler.

## 想定される欠点

Existing old eval_case records remain generic if opened directly, though they no longer pollute dossiers.

## 評価計画

Regenerate dossiers and assert they include manual eval links/scores but not ## フィクスチャ template sections under Evaluation; verify new eval cases include source-specific expected changes; run full tests and doctor.

## 中止基準

If score evidence becomes harder to find or hypotheses lose their eval link, revert to body rendering and instead require filled eval templates.


## Evidence

`harness-lab/views/eval-results/E0015-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0016: D0016: adopted H0015


Source: `harness-lab/records/decisions/D0016-adopted-h0015.md`


# D0016: adopted H0015

## 判断

adopted

## 理由

The functioning evaluation artifact is the manual eval yml/score path, while full eval case bodies were adding template noise to dossiers. Summarizing evaluation evidence keeps dossiers readable and preserves canonical eval records for linking.

## 証拠

tests/test_cli/test_mvp_flow.py asserts dossiers omit ## フィクスチャ and manual eval markdown omits the full snapshot; E0015 manual score records this change.

## 回帰リスク

Low: eval_case records remain canonical, and dossier still links source, scores, and notes.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
