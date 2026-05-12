<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0015

送信元: `harness-lab/records/eval-cases/E0015-fb0016-remove-unused-eval-case-template-noise-from-dossiers.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 2
- operator_burden: 5
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 5

## メモ

Dossiers now summarize eval records and manual eval yml/md instead of embedding full eval-case template bodies. New eval cases are seeded from source feedback summary, reproduction, and expected change. Manual eval markdown no longer includes a full eval case snapshot.

## 評価ケース

- capability: lab_evaluation_review
- failure_class: eval_template_noise_in_dossier
- source_feedback: FB0016
