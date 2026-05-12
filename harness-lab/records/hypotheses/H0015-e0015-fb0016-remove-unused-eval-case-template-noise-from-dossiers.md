---
id: H0015
record_type: hypothesis
created_at: '2026-05-13T02:32:28+09:00'
status: proposed
target_capability: lab_evaluation_review
source_eval_case: E0015
---

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
